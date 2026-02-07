import adapter from '@sveltejs/adapter-static';
import { mdsvex } from 'mdsvex';
import { createHighlighter } from 'shiki';

// Initialize Shiki highlighter
const highlighter = await createHighlighter({
	themes: ['github-dark'],
	langs: ['typescript', 'javascript', 'svelte', 'python', 'bash', 'sql', 'json', 'css', 'html', 'markdown']
});

/** @type {import('@sveltejs/kit').Config} */
const config = {
	extensions: ['.svelte', '.md'],

	preprocess: [
		mdsvex({
			extensions: ['.md'],
			highlight: {
				highlighter: (code, lang) => {
					if (!lang) lang = 'text';
					try {
						return highlighter.codeToHtml(code, { lang, theme: 'github-dark' });
					} catch {
						return `<pre><code>${code}</code></pre>`;
					}
				}
			}
		})
	],

	kit: {
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: undefined,
			precompress: false,
			strict: true
		}),
		prerender: {
			handleHttpError({ path, referrer, message }) {
				// Library content has .md cross-references that don't match SvelteKit routes
				// These will be fixed in Phase 2 (library Diátaxis restructure)
				if (path.endsWith('.md')) {
					console.warn(`[prerender] Ignoring .md link: ${path} (from ${referrer})`);
					return;
				}
				throw new Error(message);
			},
			handleMissingId: 'warn'
		},
		alias: {
			'$content': '../content'
		}
	}
};

export default config;
