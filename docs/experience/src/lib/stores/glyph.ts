import { writable } from 'svelte/store';

interface GlyphConfig {
	opacity: number;
	blur: number;
	position: string;
	visible: boolean;
}

const defaults: GlyphConfig = {
	opacity: 0.12,
	blur: 8,
	position: 'center 40%',
	visible: true
};

export const glyphConfig = writable<GlyphConfig>(defaults);

export function resetGlyph() {
	glyphConfig.set(defaults);
}

export function hideGlyph() {
	glyphConfig.update(c => ({ ...c, visible: false }));
}

export function showGlyph() {
	glyphConfig.update(c => ({ ...c, visible: true }));
}
