<script lang="ts">
	import {
		LandingComposition,
		BrandHero,
		Philosophy,
		Logo,
		QuickStart,
		NavigationCTA
	} from '../landing';
	// import { TypewriterManifesto } from '../manifesto';
</script>

<LandingComposition>
	{#snippet north()}
		<BrandHero />
	{/snippet}

	{#snippet west()}
		<Philosophy />
	{/snippet}

	{#snippet center()}
		<Logo />
	{/snippet}

	{#snippet east()}
		<NavigationCTA />
	{/snippet}

	{#snippet south()}
		<QuickStart />
	{/snippet}

</LandingComposition>
