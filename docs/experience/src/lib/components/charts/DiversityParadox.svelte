<script lang="ts">
	// Butterfly (diverging) chart encoding the diversity paradox.
	//
	// Two paired findings: individual-quality (positive, right) and
	// diversity-loss (negative, left). Center axis IS the paradox.

	type Finding = {
		source: string;
		metric: string;
		value: number;
		unit: string;
		direction: 'individual' | 'diversity';
	};

	const findings: Finding[] = [
		{ source: 'Holzner et al. 2025', metric: 'Idea diversity', value: -0.863, unit: 'g', direction: 'diversity' },
		{ source: 'Holzner et al. 2025', metric: 'Creative performance', value: +0.273, unit: 'g', direction: 'individual' },
		{ source: 'Doshi & Hauser 2024', metric: 'Collective similarity', value: -10.7, unit: '%', direction: 'diversity' },
		{ source: 'Doshi & Hauser 2024', metric: 'Individual novelty', value: +8.1, unit: '%', direction: 'individual' },
	];

	// Layout
	const W = 700;
	const rowH = 34;
	const rowGap = 6;
	const groupGap = 36;
	const topPad = 28;
	const botPad = 12;
	const H = topPad + 2 * rowH + rowGap + groupGap + 2 * rowH + rowGap + botPad;

	const pad = 12;
	const labelW = 150;
	const centerX = W / 2;
	const barZone = centerX - pad - labelW;

	// Scales
	const gMax = 1.0;
	const pctMax = 12.0;

	function barW(f: Finding): number {
		const max = f.unit === 'g' ? gMax : pctMax;
		return (Math.abs(f.value) / max) * barZone;
	}

	function rowY(i: number): number {
		if (i < 2) return topPad + i * (rowH + rowGap);
		return topPad + 2 * (rowH + rowGap) + groupGap + (i - 2) * (rowH + rowGap);
	}

	function groupLabelY(g: number): number {
		if (g === 0) return topPad - 8;
		return rowY(1) + rowH + rowGap + groupGap / 2 + 3;
	}

	const cGain = '#5a9e8a';
	const cLoss = '#c47c3a';
	const cAxis = '#333';
	const cText = '#aaa';
	const cDim = '#555';
	const cGroup = '#777';

	function valStr(f: Finding): string {
		const sign = f.value >= 0 ? '+' : '\u2212';
		return `${sign}${Math.abs(f.value)}${f.unit}`;
	}
</script>

<figure class="diversity-paradox">
	<figcaption class="chart-header">
		<span class="chart-title">Better writers. Fewer distinct ideas. Both at once.</span>
		<span class="chart-subtitle">
			Individual quality improves while collective diversity collapses — same AI, same session, opposite effects
		</span>
	</figcaption>

	<div class="chart-wrap">
		<svg viewBox="0 0 {W} {H}" role="img" aria-label="Butterfly chart: diversity paradox">
			<defs>
				<linearGradient id="dp-gl" x1="1" y1="0" x2="0" y2="0">
					<stop offset="0%" stop-color={cLoss} stop-opacity="0.2" />
					<stop offset="70%" stop-color={cLoss} stop-opacity="0.85" />
				</linearGradient>
				<linearGradient id="dp-gr" x1="0" y1="0" x2="1" y2="0">
					<stop offset="0%" stop-color={cGain} stop-opacity="0.85" />
					<stop offset="100%" stop-color={cGain} stop-opacity="0.2" />
				</linearGradient>
			</defs>

			<!-- Column headers -->
			<text x={centerX - 8} y={12} text-anchor="end" fill={cLoss} font-size="9.5" font-weight="600" letter-spacing="0.06em">COLLECTIVE DIVERSITY LOSS</text>
			<text x={centerX + 8} y={12} fill={cGain} font-size="9.5" font-weight="600" letter-spacing="0.06em">INDIVIDUAL QUALITY GAIN</text>

			<!-- Center axis -->
			<line x1={centerX} y1={20} x2={centerX} y2={H - botPad} stroke={cAxis} stroke-width="1" />

			<!-- Group labels -->
			<text x={pad} y={groupLabelY(0)} fill={cGroup} font-size="9" font-weight="600" letter-spacing="0.04em">
				HOLZNER ET AL. 2025
				<tspan fill={cDim} font-weight="400" font-size="8"> · meta-analysis · 28 studies · n=8,214</tspan>
			</text>
			<text x={pad} y={groupLabelY(1)} fill={cGroup} font-size="9" font-weight="600" letter-spacing="0.04em">
				DOSHI &amp; HAUSER 2024
				<tspan fill={cDim} font-weight="400" font-size="8"> · Science Advances · n=893</tspan>
			</text>

			<!-- Separator -->
			<line x1={pad} y1={rowY(1) + rowH + rowGap / 2} x2={W - pad} y2={rowY(1) + rowH + rowGap / 2} stroke={cAxis} stroke-width="0.5" opacity="0.4" />

			{#each findings as f, i}
				{@const y = rowY(i)}
				{@const bw = barW(f)}
				{@const isLeft = f.direction === 'diversity'}
				{@const color = isLeft ? cLoss : cGain}
				{@const grad = isLeft ? 'dp-gl' : 'dp-gr'}

				<!-- Bar -->
				<rect
					x={isLeft ? centerX - bw : centerX}
					y={y + 5}
					width={bw}
					height={rowH - 10}
					rx="2"
					fill="url(#{grad})"
				/>

				<!-- Value label inside bar (or just outside if bar is tiny) -->
				{#if isLeft}
					{@const vx = bw > 60 ? centerX - bw + 8 : centerX - bw - 6}
					{@const anchor = bw > 60 ? 'start' : 'end'}
					{@const vColor = bw > 60 ? '#fff' : color}
					<text x={vx} y={y + rowH / 2} text-anchor={anchor} dominant-baseline="central" fill={vColor} font-size="11" font-weight="700" opacity={bw > 60 ? 0.9 : 1}>{valStr(f)}</text>
				{:else}
					{@const vx = bw > 60 ? centerX + bw - 8 : centerX + bw + 6}
					{@const anchor = bw > 60 ? 'end' : 'start'}
					{@const vColor = bw > 60 ? '#fff' : color}
					<text x={vx} y={y + rowH / 2} text-anchor={anchor} dominant-baseline="central" fill={vColor} font-size="11" font-weight="700" opacity={bw > 60 ? 0.9 : 1}>{valStr(f)}</text>
				{/if}

				<!-- Metric label at outer edge -->
				{#if isLeft}
					<text x={pad + labelW - 4} y={y + rowH / 2} text-anchor="end" dominant-baseline="central" fill={cText} font-size="12">{f.metric}</text>
				{:else}
					<text x={W - pad - labelW + 4} y={y + rowH / 2} dominant-baseline="central" fill={cText} font-size="12">{f.metric}</text>
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

	.chart-wrap {
		width: 100%;
		max-width: 700px;
	}

	.chart-source {
		margin-top: 0.75rem;
		font-size: 0.7rem;
		color: #555;
	}
</style>
