<script lang="ts">
	// Butterfly (diverging) chart encoding the diversity paradox.
	//
	// Information structure: two paired findings, each with an individual-quality
	// measurement (positive, right) and a diversity-loss measurement (negative, left).
	// The center axis IS the paradox — the same AI session produces both simultaneously.
	//
	// Layout (per row):
	//   [metric label .............. bar ====] | [==== bar .............. metric label]
	//                                           ^
	//                                      center axis
	//
	// Study group labels are rendered as a small caption above each group's first row,
	// left-aligned. This avoids collision with bars. Value labels hug bar tips.

	type Finding = {
		source: string;
		metric: string;
		value: number; // negative for diversity loss, positive for individual quality
		unit: string; // 'g' (Hedges') or '%'
		direction: 'individual' | 'diversity';
	};

	// Ordered so diversity and individual rows alternate within each study group.
	// Diversity row first (top), individual row second (bottom) — loss before gain.
	const findings: Finding[] = [
		{
			source: 'Holzner et al. 2025',
			metric: 'Idea diversity',
			value: -0.863,
			unit: 'g',
			direction: 'diversity'
		},
		{
			source: 'Holzner et al. 2025',
			metric: 'Creative performance',
			value: +0.273,
			unit: 'g',
			direction: 'individual'
		},
		{
			source: 'Doshi & Hauser 2024',
			metric: 'Collective similarity',
			value: -10.7,
			unit: '%',
			direction: 'diversity'
		},
		{
			source: 'Doshi & Hauser 2024',
			metric: 'Individual novelty',
			value: +8.1,
			unit: '%',
			direction: 'individual'
		}
	];

	// SVG dimensions
	const svgWidth = 640;
	const rowHeight = 30;
	const rowGap = 8; // gap between rows within a group
	const groupGap = 32; // gap between study groups (holds the group label)
	const topPad = 44; // column headers
	const bottomPad = 12;

	// Groups: 2 rows each, with a groupGap between groups.
	// Total height: topPad + 2*(rowHeight+rowGap) + groupGap + 2*(rowHeight+rowGap) - rowGap + bottomPad
	const svgHeight =
		topPad +
		2 * rowHeight +
		1 * rowGap + // group 1: 2 rows, 1 gap between them
		groupGap + // gap between groups
		2 * rowHeight +
		1 * rowGap + // group 2
		bottomPad;

	// Horizontal layout
	// The metric label sits outside the bar zone, right-aligned to left edge of bar / left-aligned to right edge.
	// Bar zone fills from barZoneLeft to centerX (left bars) and centerX to barZoneRight (right bars).
	const outerPad = 10;
	const metricLabelWidth = 144; // reserved for metric name
	const valueLabelGap = 6; // space between bar tip and value text
	const valueLabelWidth = 48; // space for value text (e.g. "−0.863g")
	const centerX = svgWidth / 2;
	const barZoneLeft = outerPad + metricLabelWidth;
	const maxBarWidth = centerX - barZoneLeft;

	// Scales: independent per unit type
	const gMax = 1.0;
	const pctMax = 12.0;

	function scaledBarWidth(f: Finding): number {
		const abs = Math.abs(f.value);
		const max = f.unit === 'g' ? gMax : pctMax;
		return (abs / max) * maxBarWidth;
	}

	// Row y positions, accounting for groupGap between the two study groups
	function rowY(i: number): number {
		if (i < 2) {
			// Group 1: rows 0 and 1
			return topPad + i * (rowHeight + rowGap);
		} else {
			// Group 2: rows 2 and 3
			return topPad + 2 * (rowHeight + rowGap) + groupGap + (i - 2) * (rowHeight + rowGap);
		}
	}

	// Group label y positions: sit in the groupGap above each group's first row,
	// and also above group 1 (within topPad).
	function groupLabelY(groupIndex: number): number {
		// For group 0: label sits just above first row
		if (groupIndex === 0) return topPad - 10;
		// For group 1: label sits in the groupGap, below the gap midpoint
		return rowY(1) + rowHeight + rowGap + groupGap / 2 + 4;
	}

	// Colors: muted teal (individual quality gain), muted amber (diversity loss)
	const colorIndividual = '#5a9e8a';
	const colorDiversity = '#c47c3a';
	const colorAxis = '#3a3a3a';
	const colorText = '#aaa';
	const colorDimText = '#555';
	const colorGroupLabel = '#777';

	// Gradient IDs for bars (fade toward tip)
	const gradDiversity = 'dp-grad-diversity';
	const gradIndividual = 'dp-grad-individual';

	function valStr(f: Finding): string {
		const sign = f.value >= 0 ? '+' : '−';
		return `${sign}${Math.abs(f.value)}${f.unit}`;
	}
</script>

<figure class="diversity-paradox">
	<figcaption class="chart-header">
		<span class="chart-title">Better writers. Fewer distinct ideas. Both at once.</span>
		<span class="chart-subtitle">
			Individual quality improves while collective diversity collapses — same AI, same session,
			opposite effects
		</span>
	</figcaption>

	<div class="chart-container">
		<svg
			viewBox="0 0 {svgWidth} {svgHeight}"
			width="100%"
			height="100%"
			role="img"
			aria-label="Butterfly chart showing the diversity paradox. Holzner et al. 2025 (meta-analysis, 28 studies, n=8,214): idea diversity Hedges g=−0.863, creative performance Hedges g=+0.273. Doshi & Hauser 2024 (Science Advances, n=893): collective similarity +10.7% (diversity fell), individual novelty +8.1%. Left bars show loss; right bars show gain."
		>
			<defs>
				<!-- Gradient fades toward the outer tip — visual weight at center matches data weight -->
				<linearGradient id={gradDiversity} x1="1" y1="0" x2="0" y2="0">
					<stop offset="0%" stop-color={colorDiversity} stop-opacity="0.25" />
					<stop offset="60%" stop-color={colorDiversity} stop-opacity="0.88" />
				</linearGradient>
				<linearGradient id={gradIndividual} x1="0" y1="0" x2="1" y2="0">
					<stop offset="0%" stop-color={colorIndividual} stop-opacity="0.88" />
					<stop offset="100%" stop-color={colorIndividual} stop-opacity="0.25" />
				</linearGradient>
			</defs>

			<!-- ── Column headers ── -->
			<text
				x={centerX - maxBarWidth * 0.5}
				y={14}
				text-anchor="middle"
				fill={colorDiversity}
				font-size="10"
				font-family="system-ui, sans-serif"
				font-weight="600"
				letter-spacing="0.07em"
			>
				COLLECTIVE DIVERSITY LOSS
			</text>
			<text
				x={centerX + maxBarWidth * 0.5}
				y={14}
				text-anchor="middle"
				fill={colorIndividual}
				font-size="10"
				font-family="system-ui, sans-serif"
				font-weight="600"
				letter-spacing="0.07em"
			>
				INDIVIDUAL QUALITY GAIN
			</text>

			<text
				x={centerX - maxBarWidth * 0.5}
				y={26}
				text-anchor="middle"
				fill={colorDiversity}
				font-size="8.5"
				font-family="system-ui, sans-serif"
				opacity="0.5"
			>
				← extends left
			</text>
			<text
				x={centerX + maxBarWidth * 0.5}
				y={26}
				text-anchor="middle"
				fill={colorIndividual}
				font-size="8.5"
				font-family="system-ui, sans-serif"
				opacity="0.5"
			>
				extends right →
			</text>

			<!-- ── Center axis ── -->
			<line
				x1={centerX}
				y1={30}
				x2={centerX}
				y2={svgHeight - bottomPad}
				stroke={colorAxis}
				stroke-width="1"
			/>

			<!-- ── Study group labels ── -->
			<!-- Group 0: Holzner — label above first row -->
			<text
				x={outerPad}
				y={groupLabelY(0)}
				fill={colorGroupLabel}
				font-size="9"
				font-family="system-ui, sans-serif"
				font-weight="600"
				letter-spacing="0.05em"
			>
				HOLZNER ET AL. 2025
			</text>
			<text
				x={outerPad + 108}
				y={groupLabelY(0)}
				fill={colorDimText}
				font-size="8"
				font-family="system-ui, sans-serif"
			>
				· meta-analysis · 28 studies · n=8,214
			</text>

			<!-- Group 1: Doshi — label in the groupGap between groups -->
			<text
				x={outerPad}
				y={groupLabelY(1)}
				fill={colorGroupLabel}
				font-size="9"
				font-family="system-ui, sans-serif"
				font-weight="600"
				letter-spacing="0.05em"
			>
				DOSHI &amp; HAUSER 2024
			</text>
			<text
				x={outerPad + 108}
				y={groupLabelY(1)}
				fill={colorDimText}
				font-size="8"
				font-family="system-ui, sans-serif"
			>
				· Science Advances · n=893
			</text>

			<!-- ── Separator between study groups ── -->
			<line
				x1={outerPad}
				y1={rowY(1) + rowHeight + rowGap / 2}
				x2={svgWidth - outerPad}
				y2={rowY(1) + rowHeight + rowGap / 2}
				stroke={colorAxis}
				stroke-width="0.5"
				opacity="0.5"
			/>

			<!-- ── Bars, value labels, metric labels ── -->
			{#each findings as f, i}
				{@const y = rowY(i)}
				{@const bw = scaledBarWidth(f)}
				{@const isLeft = f.direction === 'diversity'}
				{@const barColor = isLeft ? colorDiversity : colorIndividual}
				{@const grad = isLeft ? gradDiversity : gradIndividual}

				<!-- Bar -->
				{#if isLeft}
					<rect
						x={centerX - bw}
						y={y + 4}
						width={bw}
						height={rowHeight - 8}
						rx="2"
						fill="url(#{grad})"
					/>
				{:else}
					<rect
						x={centerX}
						y={y + 4}
						width={bw}
						height={rowHeight - 8}
						rx="2"
						fill="url(#{grad})"
					/>
				{/if}

				<!-- Value label at bar tip -->
				{#if isLeft}
					<text
						x={centerX - bw - valueLabelGap}
						y={y + rowHeight / 2}
						text-anchor="end"
						dominant-baseline="central"
						fill={barColor}
						font-size="11"
						font-weight="700"
						font-family="system-ui, sans-serif"
					>
						{valStr(f)}
					</text>
				{:else}
					<text
						x={centerX + bw + valueLabelGap}
						y={y + rowHeight / 2}
						dominant-baseline="central"
						fill={barColor}
						font-size="11"
						font-weight="700"
						font-family="system-ui, sans-serif"
					>
						{valStr(f)}
					</text>
				{/if}

				<!-- Metric label at outer edge -->
				{#if isLeft}
					<text
						x={outerPad + metricLabelWidth}
						y={y + rowHeight / 2}
						text-anchor="end"
						dominant-baseline="central"
						fill={colorText}
						font-size="12"
						font-family="system-ui, sans-serif"
					>
						{f.metric}
					</text>
				{:else}
					<text
						x={svgWidth - outerPad - metricLabelWidth}
						y={y + rowHeight / 2}
						dominant-baseline="central"
						fill={colorText}
						font-size="12"
						font-family="system-ui, sans-serif"
					>
						{f.metric}
					</text>
				{/if}
			{/each}
		</svg>
	</div>

	<p class="chart-source">
		Holzner, Maier &amp; Feuerriegel 2025, meta-analysis 28 studies n=8,214 — Hedges' g measures
		standardized effect size. Doshi &amp; Hauser 2024, Science Advances n=893 — b=0.311 for
		collective similarity increase. Higher similarity = lower diversity.
	</p>
</figure>

<style>
	.diversity-paradox {
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
		max-width: 640px;
	}

	.chart-source {
		margin-top: 0.75rem;
		font-size: 0.7rem;
		color: #555;
	}
</style>
