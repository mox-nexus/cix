<script lang="ts">
	// Bastani et al. 2025, PNAS, n~1,000
	// Two conditions, same GPT-4 model.
	// Practice gains: GPT Base +48%, GPT Tutor +127%
	// Exam outcome vs. control: GPT Base -17%, GPT Tutor ≈0 (no significant difference)

	const svgWidth = 600;
	const svgHeight = 220;

	const margin = { top: 28, right: 16, bottom: 24, left: 16 };
	const innerW = svgWidth - margin.left - margin.right;

	// Two panels, side by side
	const panelGap = 40;
	const panelW = (innerW - panelGap) / 2;

	// Colors — one per condition, consistent across both panels
	const colorBase = '#c87060'; // warm red: performance collapse
	const colorTutor = '#6aab8a'; // muted green: learning preserved

	const barH = 28;
	const barGap = 20;
	const panelHeaderH = 24;

	function rowY(i: number): number {
		return margin.top + panelHeaderH + i * (barH + barGap);
	}

	// ─── LEFT PANEL: Practice gains ──────────────────────────────────────────
	// Layout: [condLabel 68px] [bars grow right] [value label]
	const leftStart = margin.left;
	const condLabelW = 68;
	const practiceBarAreaW = panelW - condLabelW - 40; // 40px reserved for value labels
	const practiceMax = 140;

	const practiceData = [
		{ label: 'GPT Base', value: 48, color: colorBase },
		{ label: 'GPT Tutor', value: 127, color: colorTutor }
	];

	function practiceBarW(v: number): number {
		return (v / practiceMax) * practiceBarAreaW;
	}

	// ─── RIGHT PANEL: Exam outcome vs. control ────────────────────────────────
	// Layout: [condLabel 68px] [zero axis] [bar extends LEFT from zero] [value label RIGHT of zero]
	// Zero sits at 40% of rightBarAreaW — gives enough space for -17% bar (which needs ~77% of rightBarAreaW at examAbsMax=22)
	// We cap rightBarAreaW so the bar doesn't overwhelm the panel.
	const rightStart = margin.left + panelW + panelGap;
	const rightCondLabelW = 68;
	// Right panel bar area: from after condLabel to panel end, minus value label zone
	const valueLabelZone = 36; // px reserved after zero for n.s. / value labels
	const rightBarAreaW = panelW - rightCondLabelW - valueLabelZone;
	// Zero sits at the RIGHT edge of the bar area; bars only go left (negative)
	const zeroX = rightStart + rightCondLabelW + rightBarAreaW;
	const examAbsMax = 22;

	const examData = [
		{ label: 'GPT Base', value: -17, color: colorBase, ns: false },
		{ label: 'GPT Tutor', value: 0, color: colorTutor, ns: true }
	];

	function examBarLeft(v: number): number {
		// For negative v, bar starts to the left of zero
		const scale = rightBarAreaW / examAbsMax;
		return zeroX + v * scale; // v is negative, so this is left of zero
	}
	function examBarWidth(v: number): number {
		const scale = rightBarAreaW / examAbsMax;
		return Math.abs(v) * scale;
	}

	// Panel divider
	const dividerX = margin.left + panelW + panelGap / 2;
	const axisTop = margin.top + panelHeaderH - 6;
	const axisBottom = rowY(1) + barH + 6;
</script>

<figure class="bastani-split">
	<figcaption class="chart-header">
		<span class="chart-title">Same model. Different design. Opposite outcomes.</span>
		<span class="chart-subtitle">GPT-4 Base (unrestricted) vs. GPT-4 Tutor (hints only)</span>
	</figcaption>

	<div class="chart-container">
		<svg
			viewBox="0 0 {svgWidth} {svgHeight}"
			width="100%"
			height="100%"
			role="img"
			aria-label="Two-panel chart comparing GPT-4 Base versus GPT-4 Tutor. Left panel shows practice gains: Base +48%, Tutor +127%. Right panel shows exam outcome versus a no-AI control group: Base -17%, Tutor no significant difference. Same GPT-4 model, different interaction design, opposite exam transfer outcomes."
		>
			<!-- ════════════════════════════════ -->
			<!-- LEFT PANEL — Practice gains      -->
			<!-- ════════════════════════════════ -->

			<text
				x={leftStart}
				y={margin.top + 10}
				fill="#666"
				font-size="10"
				font-family="system-ui, sans-serif"
				letter-spacing="0.06em"
			>PRACTICE GAINS</text>

			{#each practiceData as d, i}
				{@const y = rowY(i)}
				{@const bw = practiceBarW(d.value)}

				<!-- Condition label, right-aligned to bar area edge -->
				<text
					x={leftStart + condLabelW - 5}
					y={y + barH / 2}
					dominant-baseline="central"
					text-anchor="end"
					fill="#888"
					font-size="11"
					font-family="system-ui, sans-serif"
				>{d.label}</text>

				<!-- Bar -->
				<rect
					x={leftStart + condLabelW}
					y={y}
					width={bw}
					height={barH}
					rx="2"
					fill={d.color}
					opacity="0.85"
				/>

				<!-- Value label, right of bar -->
				<text
					x={leftStart + condLabelW + bw + 5}
					y={y + barH / 2}
					dominant-baseline="central"
					fill={d.color}
					font-size="13"
					font-weight="600"
					font-family="system-ui, sans-serif"
				>+{d.value}%</text>
			{/each}

			<!-- ═══════════════════════════════════════ -->
			<!-- RIGHT PANEL — Exam outcome vs. control  -->
			<!-- ═══════════════════════════════════════ -->

			<text
				x={rightStart}
				y={margin.top + 10}
				fill="#666"
				font-size="10"
				font-family="system-ui, sans-serif"
				letter-spacing="0.06em"
			>EXAM OUTCOME VS. CONTROL</text>

			<!-- Zero reference axis (bars grow leftward from here) -->
			<line
				x1={zeroX}
				y1={axisTop}
				x2={zeroX}
				y2={axisBottom}
				stroke="#444"
				stroke-width="1"
			/>

			{#each examData as d, i}
				{@const y = rowY(i)}

				<!-- Condition label -->
				<text
					x={rightStart + rightCondLabelW - 5}
					y={y + barH / 2}
					dominant-baseline="central"
					text-anchor="end"
					fill="#888"
					font-size="11"
					font-family="system-ui, sans-serif"
				>{d.label}</text>

				{#if d.ns}
					<!-- Tutor: no significant difference — tick at zero -->
					<line
						x1={zeroX}
						y1={y + barH / 2 - 10}
						x2={zeroX}
						y2={y + barH / 2 + 10}
						stroke={d.color}
						stroke-width="3"
					/>
					<!-- n.s. label right of zero -->
					<text
						x={zeroX + 6}
						y={y + barH / 2}
						dominant-baseline="central"
						fill={d.color}
						font-size="12"
						font-weight="600"
						font-family="system-ui, sans-serif"
					>n.s.</text>
				{:else}
					<!-- Base: -17% bar extending left from zero -->
					{@const bx = examBarLeft(d.value)}
					{@const bw = examBarWidth(d.value)}
					<rect
						x={bx}
						y={y}
						width={bw}
						height={barH}
						rx="2"
						fill={d.color}
						opacity="0.85"
					/>
					<!-- Value label right of zero (consistent side, unambiguous sign) -->
					<text
						x={zeroX + 6}
						y={y + barH / 2}
						dominant-baseline="central"
						fill={d.color}
						font-size="13"
						font-weight="600"
						font-family="system-ui, sans-serif"
					>{d.value}%</text>
				{/if}
			{/each}

			<!-- Zero label -->
			<text
				x={zeroX}
				y={axisBottom + 10}
				text-anchor="middle"
				fill="#555"
				font-size="10"
				font-family="system-ui, sans-serif"
			>0</text>

			<!-- Panel divider -->
			<line
				x1={dividerX}
				y1={margin.top + panelHeaderH - 10}
				x2={dividerX}
				y2={axisBottom}
				stroke="#2a2a2a"
				stroke-width="1"
			/>
		</svg>
	</div>

	<p class="chart-source">
		Source: Bastani et al. 2025, PNAS, n≈1,000. Same GPT-4 model; condition differs only in
		interaction design — unrestricted access vs. hint-only tutor. Practice gains measured within
		session. Exam outcome vs. no-AI control group. n.s. = not statistically significant.
	</p>
</figure>

<style>
	.bastani-split {
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
