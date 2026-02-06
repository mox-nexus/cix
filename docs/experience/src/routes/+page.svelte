<script lang="ts">
	import { CanonicalSigil } from '$lib/components/glyph';
	import GlyphBackground from '$lib/components/atmosphere/GlyphBackground.svelte';
</script>

<svelte:head>
	<title>cix — Collaborative Intelligence Extensions</title>
</svelte:head>

<!-- Atmospheric presence: felt, not literal -->
<GlyphBackground opacity={0.06} blur={12} />

<CanonicalSigil />
