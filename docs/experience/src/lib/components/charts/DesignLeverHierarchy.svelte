<script lang="ts">
	// Effect sizes from Blaurock et al. 2025, Journal of Service Research, N=654
	// Outcome: perceived responsibility for task outcome
	// Engagement feature is not significant (p=ns) — the critical data point
	const data = [
		{ label: 'Process control', b: 0.715, sig: true, p: 'p<.001' },
		{ label: 'Outcome control', b: 0.524, sig: true, p: 'p<.011' },
		{ label: 'Transparency', b: 0.511, sig: true, p: 'p<.001' },
		{ label: 'Engagement', b: 0.090, sig: false, p: 'ns' }
	];

	const max = 0.715; // anchored to process control — the scale is honest
	const barHeight = 32;
	const gap = 12;
	const labelWidth = 120;
	const svgWidth = 560;
	// Reserve space for value + sig label after bar (up to ~80px)
	const barAreaWidth = svgWidth - labelWidth - 80;
	const svgHeight = data.length * (barHeight + gap) - gap;

	// Divider sits between row 2 and row 3 (0-indexed) — separates sig from null
	const dividerY = 3 * (barHeight + gap) - gap / 2;

	// Significant bars match site's spark blue
	const sigFill = '#7eb8da';

	function xForB(b: number): number {
		return (b / max) * barAreaWidth;
	}
</script>

<figure class="design-lever-hierarchy">
	<figcaption class="chart-header">
		<span class="chart-title">Control features dominate. Engagement features don't work.</span>
		<span class="chart-subtitle"
			>Effect on perceived outcome responsibility — four AI design features, ranked</span
		>
	</figcaption>

	<div class="chart-container">
		<svg
			viewBox="0 0 {svgWidth} {svgHeight}"
			width="100%"
			height="100%"
			role="img"
			aria-label="Horizontal bar chart ranking four AI design features by effect size on perceived outcome responsibility. Process control: b=0.715 (p<.001). Outcome control: b=0.524 (p<.011). Transparency: b=0.511 (p<.001). Engagement: b=0.090 (not significant). The engagement bar is visually distinct — dashed outline with hatching — marking its null result. Control features are 6–8x larger in effect."
		>
			<!-- Hatch pattern for the null bar — defined before use -->
			<defs>
				<pattern
					id="null-hatch"
					patternUnits="userSpaceOnUse"
					width="6"
					height="6"
					patternTransform="rotate(45)"
				>
					<line x1="0" y1="0" x2="0" y2="6" stroke="#3a3a3a" stroke-width="1.5" />
				</pattern>
			</defs>

			{#each data as d, i}
				{@const y = i * (barHeight + gap)}
				{@const bw = xForB(d.b)}

				<!-- Feature label -->
				<text
					x={labelWidth - 10}
					y={y + barHeight / 2}
					text-anchor="end"
					dominant-baseline="central"
					fill={d.sig ? '#aaa' : '#555'}
					font-size="13"
					font-family="system-ui, sans-serif"
				>
					{d.label}
				</text>

				<!-- Bar: filled for significant, dashed outline for null -->
				{#if d.sig}
					<rect
						x={labelWidth}
						{y}
						width={bw}
						height={barHeight}
						rx="3"
						fill={sigFill}
						opacity="0.85"
					/>
				{:else}
					<!-- Hatch fill — encodes "no result here", not decoration -->
					<rect
						x={labelWidth}
						{y}
						width={bw}
						height={barHeight}
						rx="3"
						fill="url(#null-hatch)"
					/>
					<!-- Dashed stroke — same geometry, categorically different treatment -->
					<rect
						x={labelWidth}
						{y}
						width={bw}
						height={barHeight}
						rx="3"
						fill="none"
						stroke="#555"
						stroke-width="1.5"
						stroke-dasharray="5,3"
					/>
				{/if}

				<!-- Effect size value -->
				<text
					x={labelWidth + bw + 8}
					y={y + barHeight / 2}
					dominant-baseline="central"
					fill={d.sig ? sigFill : '#555'}
					font-size="12"
					font-weight={d.sig ? '600' : '400'}
					font-family="system-ui, sans-serif"
				>
					{d.b.toFixed(3)}
				</text>

				<!-- Significance marker — italic 'ns' distinguishes without relying on color alone -->
				<text
					x={labelWidth + bw + 46}
					y={y + barHeight / 2}
					dominant-baseline="central"
					fill={d.sig ? '#6a8fa0' : '#444'}
					font-size="10"
					font-family="system-ui, sans-serif"
					font-style={d.sig ? 'normal' : 'italic'}
				>
					{d.p}
				</text>
			{/each}

			<!-- Divider before the null row — the line that says "below this, nothing lands" -->
			<line
				x1={labelWidth}
				y1={dividerY}
				x2={svgWidth - 4}
				y2={dividerY}
				stroke="#2e2e2e"
				stroke-width="1"
			/>
		</svg>
	</div>

	<p class="chart-source">
		Blaurock, M., et al. (2025). Designing Responsible AI. <em>Journal of Service Research</em>.
		N=654. Regression coefficients (b) on perceived outcome responsibility. Engagement
		(p=.346) is not significant. Dashed bar marks the null.
	</p>
</figure>

<style>
	.design-lever-hierarchy {
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
		margin-bottom: 1.25rem;
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
		max-width: 560px;
	}

	.chart-source {
		margin-top: 0.75rem;
		font-size: 0.7rem;
		color: #555;
		line-height: 1.5;
	}
</style>
