<script lang="ts">
	import type { PageData } from './$types';
	import { ArticleShell } from '$lib/components/library';

	let { data }: { data: PageData } = $props();
</script>

<ArticleShell
	quadrant="reference"
	content={data.content}
	metadata={data.metadata}
	position={data.position}
	total={data.total}
	prev={data.prev}
	next={data.next}
/>
