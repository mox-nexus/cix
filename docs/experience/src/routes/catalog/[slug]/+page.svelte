<script lang="ts">
	import type { PageData } from './$types';
	import { PluginDetail } from '$lib/components/catalog';

	let { data }: { data: PageData } = $props();
</script>

<svelte:head>
	<title>{data.extension.slug} — cix</title>
	<meta name="description" content={data.extension.manifest.description} />
</svelte:head>

<PluginDetail extension={data.extension} />
