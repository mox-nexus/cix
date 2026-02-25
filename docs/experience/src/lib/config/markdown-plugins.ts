import type { Plugin } from 'svelte-exmarkdown';
import { gfmPlugin } from 'svelte-exmarkdown/gfm';
import rehypeSlug from 'rehype-slug';
import rehypeRaw from 'rehype-raw';
import rehypeShikiFromHighlighter from '@shikijs/rehype/core';
import { createHighlighter } from 'shiki';

const highlighter = await createHighlighter({
	themes: ['github-dark'],
	langs: [
		'typescript',
		'javascript',
		'svelte',
		'python',
		'bash',
		'sql',
		'json',
		'css',
		'html',
		'markdown'
	]
});

export const plugins: Plugin[] = [
	gfmPlugin(),
	{ rehypePlugin: [rehypeRaw] },
	{ rehypePlugin: [rehypeSlug] },
	{
		rehypePlugin: [
			rehypeShikiFromHighlighter,
			highlighter,
			{ theme: 'github-dark' }
		]
	}
];
