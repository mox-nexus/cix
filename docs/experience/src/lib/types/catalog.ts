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

export type LifecyclePhase =
	| 'research'
	| 'understand'
	| 'design'
	| 'craft'
	| 'measure'
	| 'foundation'
	| 'tools';

export interface CatalogExtension {
	slug: string;
	kind: 'plugin' | 'tool';
	manifest: PluginManifest;
	tagline: string;
	readme: string;
	components: PluginComponents;
	variant: 'spark' | 'emergence' | 'constraint';
	tags: string[];
	phase: LifecyclePhase;
}
