<script lang="ts">
	import { LIBRARY, CLUSTERS, getClusterEntries } from '$lib/data/library';
	import type { Cluster } from '$lib/data/library';
	import { readingProgress, readingOverview } from '$lib/stores/reading-progress';
	import { base } from '$app/paths';
	import { CrossLinks } from '$lib/components/nav';

	const DIFFICULTY_ICON: Record<string, string> = {
		foundational: '○',
		intermediate: '◐',
		advanced: '●'
	};

	const STATE_ICON: Record<string, string> = {
		unvisited: '○',
		visited: '◐',
		completed: '●'
	};

	let overview = $derived($readingOverview);
	let totalArticles = $derived(
		LIBRARY.find((q) => q.id === 'explanation')?.entries.length ?? 0
	);
	let progress = $derived($readingProgress);

	function entryState(slug: string): string {
		return progress.entries[slug] || 'unvisited';
	}

	function clusterProgress(clusterId: Cluster) {
		const entries = getClusterEntries(clusterId);
		const completed = entries.filter((e) => entryState(e.slug) === 'completed').length;
		const visited = entries.filter((e) => entryState(e.slug) !== 'unvisited').length;
		return { completed, visited, total: entries.length };
	}

	let reference = $derived(LIBRARY.find((q) => q.id === 'reference'));
</script>

<svelte:head>
	<title>Library — cix</title>
	<meta
		name="description"
		content="Research and practice of collaborative intelligence. 13 articles organized by topic cluster."
	/>
</svelte:head>

<div class="library-index">
	<header class="library-header">
		<h1>Library</h1>
		<p class="intro">
			The research behind collaborative intelligence — organized by topic,
			ordered for progressive understanding.
		</p>
	</header>

	<!-- Reading progress overview -->
	<div class="progress-overview">
		<div class="progress-bar" aria-label="Reading progress">
			<div
				class="progress-fill"
				style="width: {totalArticles ? (overview.completed / totalArticles) * 100 : 0}%"
			></div>
			<div
				class="progress-visited"
				style="width: {totalArticles ? ((overview.completed + overview.visited) / totalArticles) * 100 : 0}%"
			></div>
		</div>
		<span class="progress-label">
			{overview.completed} of {totalArticles} read
			{#if overview.visited > 0}
				· {overview.visited} in progress
			{/if}
		</span>
	</div>

	<!-- Cluster navigation strip -->
	<nav class="cluster-strip" aria-label="Topic clusters">
		{#each CLUSTERS as cluster}
			{@const cp = clusterProgress(cluster.id)}
			<a href="#{cluster.id}" class="cluster-chip">
				<span class="chip-label">{cluster.label}</span>
				<span class="chip-progress">{cp.completed}/{cp.total}</span>
			</a>
		{/each}
	</nav>

	<!-- Suggested start (shown for first-time visitors) -->
	{#if overview.completed === 0 && overview.visited <= 1}
		<div class="suggested-start">
			<span class="suggested-label">start here</span>
			<a href="{base}/library/explanation/what-is-ci" class="suggested-link">
				<span class="suggested-title">What is CI</span>
				<span class="suggested-desc">The collaborative intelligence thesis · 5 min</span>
			</a>
		</div>
	{/if}

	<!-- Cluster sections -->
	{#each CLUSTERS as cluster}
		{@const entries = getClusterEntries(cluster.id)}
		{@const cp = clusterProgress(cluster.id)}
		<section id={cluster.id} class="cluster-section">
			<div class="cluster-header">
				<h2 class="cluster-label">{cluster.label}</h2>
				<p class="cluster-description">{cluster.description}</p>
				<span class="cluster-progress-text">{cp.completed}/{cp.total}</span>
			</div>

			<nav class="cluster-entries" aria-label="{cluster.label} articles">
				{#each entries as entry, i}
					{@const state = entryState(entry.slug)}
					<a
						href="{base}/library/explanation/{entry.slug}"
						class="cluster-entry"
						class:is-completed={state === 'completed'}
						class:is-visited={state === 'visited'}
					>
						<span class="entry-index">{i + 1}</span>
						<div class="entry-body">
							<div class="entry-top">
								<span class="entry-title">{entry.title}</span>
								<span class="entry-meta">
									{#if entry.readMinutes}{entry.readMinutes} min{/if}
									{#if entry.difficulty}
										<span class="entry-difficulty" title={entry.difficulty}>
											{DIFFICULTY_ICON[entry.difficulty]}
										</span>
									{/if}
								</span>
							</div>
							<span class="entry-description">{entry.description}</span>
						</div>
						<span class="entry-state" title={state}>
							{STATE_ICON[state]}
						</span>
					</a>
					{#if i < entries.length - 1}
						<div class="entry-connector" aria-hidden="true"></div>
					{/if}
				{/each}
			</nav>
		</section>
	{/each}

	<!-- Reference section -->
	{#if reference && reference.entries.length > 0}
		<section id="reference" class="reference-section">
			<div class="cluster-header">
				<h2 class="cluster-label">Reference</h2>
				<p class="cluster-description">{reference.tagline}</p>
			</div>
			{#each reference.entries as entry}
				<a href="{base}/library/reference/{entry.slug}" class="ref-link">
					<span class="ref-title">{entry.title}</span>
					<span class="ref-description">{entry.description}</span>
				</a>
			{/each}
		</section>
	{/if}

	<CrossLinks />
</div>

<style>
	.library-index {
		max-width: 72ch;
		margin: 0 auto;
	}

	/* --- Header --- */

	.library-header {
		margin-bottom: var(--space-3);
	}

	.library-header h1 {
		font-size: var(--type-xl);
		margin: 0 0 var(--space-1) 0;
	}

	.intro {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		line-height: var(--leading-relaxed);
		margin: 0;
	}

	/* --- Progress Overview --- */

	.progress-overview {
		display: flex;
		align-items: center;
		gap: var(--space-2);
		margin-bottom: var(--space-3);
	}

	.progress-bar {
		flex: 1;
		height: 4px;
		background: var(--dao-surface);
		border-radius: 2px;
		position: relative;
		overflow: hidden;
	}

	.progress-visited {
		position: absolute;
		inset: 0;
		background: var(--dao-border);
		border-radius: 2px;
		transition: width var(--duration-normal) var(--easing-enter);
	}

	.progress-fill {
		position: absolute;
		inset: 0;
		background: var(--spark-core);
		border-radius: 2px;
		z-index: 1;
		transition: width var(--duration-normal) var(--easing-enter);
	}

	.progress-label {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
		white-space: nowrap;
	}

	/* --- Cluster Strip --- */

	.cluster-strip {
		display: flex;
		gap: var(--space-2);
		padding-bottom: var(--space-2);
		border-bottom: 1px solid var(--dao-border-subtle);
		margin-bottom: var(--space-4);
		flex-wrap: wrap;
	}

	.cluster-chip {
		font-family: var(--font-sans);
		font-size: var(--type-xs);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		color: var(--dao-muted);
		text-decoration: none;
		display: inline-flex;
		align-items: center;
		gap: var(--space-1);
		transition: color var(--duration-fast) var(--easing-linear);
	}

	.cluster-chip:hover {
		color: var(--dao-text);
	}

	.chip-progress {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		opacity: 0.5;
	}

	/* --- Suggested Start --- */

	.suggested-start {
		background: var(--dao-surface);
		border: 1px solid var(--dao-border);
		border-left: 3px solid var(--spark-core);
		border-radius: var(--radius-sm);
		padding: var(--space-2) var(--space-3);
		margin-bottom: var(--space-4);
	}

	.suggested-label {
		font-family: var(--font-sans);
		font-size: var(--type-xs);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		color: var(--spark-core);
		display: block;
		margin-bottom: var(--space-1);
	}

	.suggested-link {
		text-decoration: none;
		display: block;
	}

	.suggested-title {
		font-family: var(--font-sans);
		font-size: var(--type-base);
		font-weight: 600;
		color: var(--dao-text);
		display: block;
	}

	.suggested-desc {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
	}

	/* --- Cluster Sections --- */

	.cluster-section {
		margin-bottom: var(--space-4);
	}

	.reference-section {
		margin-bottom: var(--space-4);
	}

	.cluster-header {
		margin-bottom: var(--space-2);
		padding-bottom: var(--space-1);
		border-bottom: 1px solid var(--dao-border-subtle);
		display: flex;
		align-items: baseline;
		gap: var(--space-2);
		flex-wrap: wrap;
	}

	.cluster-label {
		font-family: var(--font-sans);
		font-size: var(--type-xs);
		text-transform: uppercase;
		letter-spacing: var(--tracking-widest);
		color: var(--dao-text-secondary);
		margin: 0;
		font-weight: 600;
	}

	.cluster-description {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		margin: 0;
		flex: 1;
	}

	.cluster-progress-text {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
		opacity: 0.5;
	}

	/* --- Cluster Entries --- */

	.cluster-entries {
		display: flex;
		flex-direction: column;
	}

	.cluster-entry {
		display: flex;
		align-items: flex-start;
		gap: var(--space-2);
		padding: var(--space-1-5) var(--space-1);
		text-decoration: none;
		border-radius: var(--radius-sm);
		transition: background var(--duration-fast) var(--easing-linear);
	}

	.cluster-entry:hover {
		background: var(--dao-surface);
	}

	.entry-index {
		font-family: var(--font-mono);
		font-size: var(--type-lg);
		font-weight: 700;
		color: var(--dao-border);
		min-width: 2ch;
		text-align: right;
		line-height: 1.2;
	}

	.cluster-entry.is-visited .entry-index {
		color: var(--dao-text-secondary);
	}

	.cluster-entry.is-completed .entry-index {
		color: var(--spark-core);
	}

	.entry-body {
		flex: 1;
		min-width: 0;
	}

	.entry-top {
		display: flex;
		align-items: baseline;
		gap: var(--space-2);
		margin-bottom: 2px;
	}

	.entry-title {
		font-family: var(--font-sans);
		font-size: var(--type-base);
		font-weight: 600;
		color: var(--dao-text);
	}

	.entry-meta {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
		display: flex;
		align-items: center;
		gap: 0.5ch;
		white-space: nowrap;
	}

	.entry-difficulty {
		font-size: 0.7em;
	}

	.entry-description {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		line-height: var(--leading-relaxed);
	}

	.entry-state {
		font-size: var(--type-sm);
		color: var(--dao-border);
		min-width: 1.5ch;
		text-align: center;
		line-height: 1.4;
	}

	.cluster-entry.is-visited .entry-state {
		color: var(--dao-text-secondary);
	}

	.cluster-entry.is-completed .entry-state {
		color: var(--spark-core);
	}

	.entry-connector {
		width: 2px;
		height: var(--space-1);
		background: var(--dao-border-subtle);
		margin-left: calc(1ch + var(--space-1));
	}

	/* --- Reference Link --- */

	.ref-link {
		display: block;
		padding: var(--space-2);
		background: var(--dao-surface);
		border: 1px solid var(--dao-border);
		border-left: 3px solid var(--dao-text-secondary);
		border-radius: var(--radius-sm);
		text-decoration: none;
		transition: border-color var(--duration-fast) var(--easing-linear);
	}

	.ref-link:hover {
		border-color: var(--dao-text-secondary);
	}

	.ref-title {
		display: block;
		font-family: var(--font-sans);
		font-size: var(--type-base);
		font-weight: 600;
		color: var(--dao-text);
		margin-bottom: 2px;
	}

	.ref-description {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
	}

	/* --- Reduced Motion --- */

	@media (prefers-reduced-motion: reduce) {
		.cluster-entry,
		.ref-link,
		.cluster-chip,
		.progress-fill,
		.progress-visited {
			transition: none;
		}
	}
</style>
