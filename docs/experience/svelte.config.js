import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
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
				// Relative links in rendered README/docs markdown can escape the base path
				if (message.includes('does not begin with `base`')) {
					console.warn(`[prerender] Ignoring out-of-base link: ${path} (from ${referrer})`);
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
