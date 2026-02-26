<script lang="ts">
	// Growth rate: (2024-26 annual creation rate) / (2016-22 annual creation rate)
	// Baseline GitHub growth (app, project): ~1.5×
	const data = [
		{ name: 'Nexus', rate: 15.7, repos: '49K' },
		{ name: 'Pulse', rate: 14.2, repos: '43K' },
		{ name: 'Aegis', rate: 13.0, repos: '5K' },
		{ name: 'Sentinel', rate: 9.7, repos: '19K' },
		{ name: 'Nova', rate: 8.3, repos: '44K' },
		{ name: 'Apex', rate: 7.2, repos: '24K' },
		{ name: 'Quantum', rate: 6.8, repos: '39K' },
		{ name: 'Cortex', rate: 6.8, repos: '6K' },
		{ name: 'Synapse', rate: 6.1, repos: '6K' },
		{ name: 'Flux', rate: 5.3, repos: '26K' }
	];

	const baseline = 1.5;
	const max = Math.max(...data.map((d) => d.rate));
	const barHeight = 28;
	const gap = 6;
	const labelWidth = 80;
	const rateWidth = 80;
	const chartLeft = labelWidth;
	const chartRight = 10;
	const svgWidth = 600;
	const barAreaWidth = svgWidth - chartLeft - chartRight - rateWidth;
	const svgHeight = data.length * (barHeight + gap) - gap + 20;
	const baselineX = chartLeft + (baseline / max) * barAreaWidth;

	function barWidth(rate: number): number {
		return (rate / max) * barAreaWidth;
	}
</script>

<figure class="naming-convergence">
	<figcaption class="chart-header">
		<span class="chart-title">Name collision is accelerating in the AI era</span>
		<span class="chart-subtitle"
			>Annual repo creation rate (2024–26) vs baseline (2016–22)</span
		>
	</figcaption>

	<div class="chart-container">
		<svg
			viewBox="0 0 {svgWidth} {svgHeight}"
			width="100%"
			height="100%"
			role="img"
			aria-label="Bar chart showing growth rate of GitHub repo names: Nexus 15.7x, Pulse 14.2x, Aegis 13.0x, Sentinel 9.7x, Nova 8.3x, Apex 7.2x, Quantum 6.8x, Cortex 6.8x, Synapse 6.1x, Flux 5.3x. Baseline GitHub growth is 1.5x."
		>
			<!-- Baseline reference line -->
			<line
				x1={baselineX}
				y1={-4}
				x2={baselineX}
				y2={svgHeight - 8}
				stroke="#555"
				stroke-width="1"
				stroke-dasharray="4,3"
			/>
			<text
				x={baselineX}
				y={svgHeight - 2}
				text-anchor="middle"
				fill="#666"
				font-size="10"
				font-family="system-ui, sans-serif"
			>
				baseline 1.5×
			</text>

			{#each data as d, i}
				{@const y = i * (barHeight + gap)}
				<!-- Label -->
				<text
					x={chartLeft - 8}
					y={y + barHeight / 2}
					text-anchor="end"
					dominant-baseline="central"
					fill="#aaa"
					font-size="13"
					font-family="system-ui, sans-serif"
				>
					{d.name}
				</text>

				<!-- Bar -->
				<rect
					x={chartLeft}
					{y}
					width={barWidth(d.rate)}
					height={barHeight}
					rx="3"
					fill="#7eb8da"
					opacity={0.85}
				/>

				<!-- Rate -->
				<text
					x={chartLeft + barWidth(d.rate) + 6}
					y={y + barHeight / 2}
					dominant-baseline="central"
					fill="#7eb8da"
					font-size="12"
					font-weight="600"
					font-family="system-ui, sans-serif"
				>
					{d.rate}×
				</text>

				<!-- Repo count -->
				<text
					x={chartLeft + barWidth(d.rate) + 46}
					y={y + barHeight / 2}
					dominant-baseline="central"
					fill="#666"
					font-size="11"
					font-family="system-ui, sans-serif"
				>
					({d.repos})
				</text>
			{/each}
		</svg>
	</div>

	<p class="chart-source">
		Source: GitHub Search API, February 2026. Rate = (2024–26 repos/yr) ÷ (2016–22
		repos/yr). Baseline: "app" and "project" grew ~1.5×.
	</p>
</figure>

<style>
	.naming-convergence {
		margin: 2rem 0;
		padding: 1.5rem;
		background: var(--chart-bg, #1a1a1a);
		border-radius: 8px;
		border: 1px solid #2a2a2a;
	}

	.chart-header {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
		margin-bottom: 1rem;
	}

	.chart-title {
		font-size: 0.9rem;
		font-weight: 600;
		color: #e8e8e8;
	}

	.chart-subtitle {
		font-size: 0.8rem;
		color: #888;
	}

	.chart-container {
		width: 100%;
		max-width: 600px;
	}

	.chart-source {
		margin-top: 0.75rem;
		font-size: 0.7rem;
		color: #555;
	}
</style>
