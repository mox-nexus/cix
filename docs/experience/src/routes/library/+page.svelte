<script lang="ts">
	import { ChevronRight } from 'lucide-svelte';
</script>

<svelte:head>
	<title>Library — cix</title>
</svelte:head>

<h1>Library</h1>
<p class="intro">Deep-dive documentation on collaborative intelligence research, principles, and patterns.</p>

<section class="section">
	<h2>Explanation</h2>
	<p>Understanding the why behind collaborative intelligence design.</p>

	<div class="card-grid">
		<a href="/library/explanation/the-problem" class="doc-card">
			<h3>The Problem</h3>
			<p>AI improves task performance while degrading capability.</p>
			<span class="card-link">Read <ChevronRight size={14} /></span>
		</a>

		<a href="/library/explanation/the-evidence" class="doc-card">
			<h3>The Evidence</h3>
			<p>Research synthesis from CHI, PNAS, and premier venues.</p>
			<span class="card-link">Read <ChevronRight size={14} /></span>
		</a>

		<a href="/library/explanation/why-it-matters" class="doc-card">
			<h3>Why It Matters</h3>
			<p>Stakes of getting collaborative intelligence right.</p>
			<span class="card-link">Read <ChevronRight size={14} /></span>
		</a>

		<a href="/library/explanation/skill-formation" class="doc-card">
			<h3>Skill Formation</h3>
			<p>How expertise develops and what threatens it.</p>
			<span class="card-link">Read <ChevronRight size={14} /></span>
		</a>

		<a href="/library/explanation/first-principles" class="doc-card">
			<h3>First Principles</h3>
			<p>Core design principles for complementary AI.</p>
			<span class="card-link">Read <ChevronRight size={14} /></span>
		</a>
	</div>
</section>

<section class="section">
	<h2>Reference</h2>
	<p>Sources and citations.</p>

	<div class="card-grid">
		<a href="/library/reference/bibliography" class="doc-card">
			<h3>Bibliography</h3>
			<p>Full citation list for all research referenced.</p>
			<span class="card-link">View <ChevronRight size={14} /></span>
		</a>
	</div>
</section>

<style>
	.intro {
		font-size: var(--type-base);
		color: var(--dao-muted);
		margin-bottom: var(--space-4);
	}

	.section {
		margin-bottom: var(--space-4);
	}

	.section h2 {
		font-size: var(--type-lg);
		margin-bottom: var(--space-1);
	}

	.section > p {
		color: var(--dao-muted);
		margin-bottom: var(--space-2);
	}

	.card-grid {
		display: grid;
		gap: var(--space-2);
	}

	.doc-card {
		display: block;
		padding: var(--space-2);
		background: var(--dao-surface);
		border: var(--border-width) solid var(--dao-border);
		border-radius: var(--radius-sm);
		text-decoration: none;
		transition: border-color var(--duration-fast) var(--easing-linear);
	}

	.doc-card:hover {
		border-color: var(--dao-blue);
	}

	.doc-card h3 {
		font-size: var(--type-base);
		margin: 0 0 var(--space-1);
		color: var(--dao-text);
	}

	.doc-card p {
		font-size: var(--type-sm);
		color: var(--dao-muted);
		margin: 0;
	}

	.card-link {
		display: inline-flex;
		align-items: center;
		gap: 4px;
		margin-top: var(--space-1);
		font-size: var(--type-sm);
		color: var(--dao-blue);
	}

	@media (min-width: 600px) {
		.card-grid {
			grid-template-columns: repeat(2, 1fr);
		}
	}
</style>
