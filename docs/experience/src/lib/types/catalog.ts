export interface PluginComponents {
	agents: number;
	skills: number;
	hooks: number;
	commands: number;
}

export interface PluginManifest {
	name: string;
	version: string;
	description: string;
	keywords?: string[];
	author: { name: string; email?: string };
	license?: string;
}

export interface DocEntry {
	slug: string;
	title: string;
	content: string;
}

export type DocCategory = 'explanation' | 'how-to' | 'tutorials';

export type ExtensionDocs = Record<DocCategory, DocEntry[]>;

export interface CatalogExtension {
	slug: string;
	kind: 'plugin' | 'tool';
	manifest: PluginManifest;
	tagline: string;
	readme: string;
	components: PluginComponents;
	variant: 'spark' | 'emergence' | 'constraint';
	tags: string[];
	docs?: ExtensionDocs;
	docCount: number;
}
