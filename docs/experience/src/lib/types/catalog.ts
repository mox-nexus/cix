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

export interface CatalogPlugin {
	slug: string;
	manifest: PluginManifest;
	tagline: string;
	readme: string;
	components: PluginComponents;
	variant: 'spark' | 'emergence' | 'constraint';
	narrativeHook?: string;
	constraint?: string;
}
