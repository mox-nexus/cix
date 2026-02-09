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
					// Escape characters that Svelte would interpret as expressions or tags.
					// Without this, {curlies} in code blocks become Svelte expressions
					// and <angle brackets> become component tags — breaking the build.
					const escapeSvelte = (html) =>
						html.replace(/\{/g, '&#123;').replace(/\}/g, '&#125;');
					try {
						return escapeSvelte(highlighter.codeToHtml(code, { lang, theme: 'github-dark' }));
					} catch {
						const escaped = code.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
						return escapeSvelte(`<pre><code>${escaped}</code></pre>`);
					}
				}
			}
		})
	],

	kit: {
		paths: {
			base: process.env.BASE_PATH || ''
		},
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: undefined,
			precompress: false,
			strict: true
		}),
		prerender: {
			handleHttpError({ path, referrer, message }) {
				// Library markdown may contain .md cross-references that don't match routes
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
