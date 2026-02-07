<script lang="ts">
	import { onMount } from 'svelte';

	interface Props {
		showCage?: boolean;
		maxSize?: string;
	}

	let { showCage = true, maxSize = '100%' }: Props = $props();

	// Animation state
	let time = $state(0);
	let entities = $state([
		{ id: 0, progress: 0 },
		{ id: 1, progress: 0.25 },
		{ id: 2, progress: 0.5 },
		{ id: 3, progress: 0.75 },
	]);

	const canvasSize = 400;
	const center = canvasSize / 2;
	const spiralStart = 55;
	const spiralEnd = 115;
	const spiralTurns = 1.1;

	onMount(() => {
		let animationId: number;
		let lastTime = performance.now();

		const animate = (currentTime: number) => {
			const delta = currentTime - lastTime;
			lastTime = currentTime;
			time += delta;

			const speed = 0.00008;
			entities = entities.map(v => ({
				...v,
				progress: (v.progress + speed * delta) % 1
			}));

			animationId = requestAnimationFrame(animate);
		};

		animationId = requestAnimationFrame(animate);
		return () => cancelAnimationFrame(animationId);
	});

	// Spiral position + stage for each entity
	function getTransform(progress: number, t: number) {
		const angle = -Math.PI / 2 + progress * spiralTurns * 2 * Math.PI;
		const distance = spiralStart + progress * (spiralEnd - spiralStart);
		const x = center + Math.cos(angle) * distance;
		const y = center + Math.sin(angle) * distance;
		const stage = Math.min(4, Math.floor(progress * 4) + 1);
		const size = 12 + progress * 16;

		let opacity = 1;
		if (progress < 0.1) opacity = progress / 0.1;
		if (progress > 0.85) opacity = (1 - progress) / 0.15;

		const rotation = -(t * 0.05) % 360;
		return { x, y, stage, size, opacity, rotation };
	}

	// d-arm primitive: circle + stem at given angle
	function getDArm(angle: number, circR: number, stemLen: number) {
		const ex = Math.cos(angle) * circR;
		const ey = Math.sin(angle) * circR;
		const tx = Math.cos(angle) * (circR + stemLen);
		const ty = Math.sin(angle) * (circR + stemLen);
		return { circR, ex, ey, tx, ty };
	}

	// Emergence stage geometry (replaces valknut triangles)
	function getEmergenceArms(stage: number, size: number) {
		const sw = Math.max(1, 2 - stage * 0.25);

		if (stage <= 1) {
			return { arms: [getDArm(0, size * 0.3, size * 0.5)], sw, circR: size * 0.3, centers: [] };
		}
		if (stage === 2) {
			const arms = [0, 120, 240].map(d => getDArm(d * Math.PI / 180, size * 0.22, size * 0.42));
			return { arms, sw, circR: size * 0.22, centers: [{ r: 1.2 }] };
		}
		if (stage === 3) {
			const arms = [0, 60].flatMap(off =>
				[0, 120, 240].map(d => getDArm((d + off) * Math.PI / 180, size * 0.19, size * 0.38))
			);
			return { arms, sw, circR: size * 0.19, centers: [{ r: 1.4 }] };
		}
		// stage 4 — fractal recursion
		const cr = size * 0.15;
		const sl = size * 0.3;
		const mr = size * 0.055;
		const ml = size * 0.11;
		const msw = Math.max(0.4, sw * 0.5);
		const arms: ReturnType<typeof getDArm>[] = [];
		const microArms: { parentX: number; parentY: number; arm: ReturnType<typeof getDArm> }[] = [];

		for (const off of [0, 30, 60, 90]) {
			for (const d of [0, 120, 240]) {
				const a = (d + off) * Math.PI / 180;
				arms.push(getDArm(a, cr, sl));
				const parentX = Math.cos(a) * (cr + sl);
				const parentY = Math.sin(a) * (cr + sl);
				for (const sd of [0, 120, 240]) {
					microArms.push({
						parentX,
						parentY,
						arm: getDArm((sd + d + off) * Math.PI / 180, mr, ml)
					});
				}
			}
		}
		return { arms, sw, circR: cr, centers: [{ r: 1.8 }], microArms, msw, microCircR: mr };
	}

	// Spark rays (pulsing 6-ray star)
	function getSparkRays(t: number) {
		const rays = [];
		for (let i = 0; i < 6; i++) {
			const angle = (i * 60 - 90) * Math.PI / 180;
			const isLong = i % 2 === 0;
			const pulse = Math.sin(t * 0.005 + (isLong ? 0 : Math.PI));
			const baseLen = isLong ? 20 : 12;
			const length = baseLen + pulse * 4;
			rays.push({
				x2: center + Math.cos(angle) * length,
				y2: center + Math.sin(angle) * length,
				width: isLong ? 2.5 : 1.5
			});
		}
		return rays;
	}

	// Heptagon vertices (replaces gear)
	function getHeptagon(radius: number, t: number) {
		const n = 7;
		const rotation = (t * 0.02) % 360;
		const verts = Array.from({ length: n }, (_, i) => {
			const a = (i / n) * 2 * Math.PI - Math.PI / 2;
			return { x: Math.cos(a) * radius, y: Math.sin(a) * radius };
		});
		const outline = verts.map((v, i) =>
			`${i === 0 ? 'M' : 'L'} ${v.x} ${v.y}`
		).join(' ') + ' Z';
		const star = Array.from({ length: n }, (_, i) => {
			const v = verts[(i * 2) % 7];
			return `${i === 0 ? 'M' : 'L'} ${v.x} ${v.y}`;
		}).join(' ') + ' Z';
		return { outline, star, verts, rotation };
	}

	let sparkRays = $derived(getSparkRays(time));
	let heptagon = $derived(getHeptagon(25, time));
</script>

<div class="sigil-container">
	{#if showCage}
		<div class="cage-line north"></div>
		<div class="cage-line south"></div>
		<div class="cage-line west"></div>
		<div class="cage-line east"></div>
	{/if}

	<svg viewBox="0 0 {canvasSize} {canvasSize}" class="sigil">
		<defs>
			<filter id="spark-glow" x="-100%" y="-100%" width="300%" height="300%">
				<feGaussianBlur in="SourceGraphic" stdDeviation="2" result="blur1"/>
				<feGaussianBlur in="SourceGraphic" stdDeviation="6" result="blur2"/>
				<feGaussianBlur in="SourceGraphic" stdDeviation="12" result="blur3"/>
				<feMerge>
					<feMergeNode in="blur3"/>
					<feMergeNode in="blur2"/>
					<feMergeNode in="blur1"/>
					<feMergeNode in="SourceGraphic"/>
				</feMerge>
			</filter>
			<filter id="emergence-glow" x="-50%" y="-50%" width="200%" height="200%">
				<feGaussianBlur in="SourceGraphic" stdDeviation="1.5" result="blur1"/>
				<feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur2"/>
				<feMerge>
					<feMergeNode in="blur2"/>
					<feMergeNode in="blur1"/>
					<feMergeNode in="SourceGraphic"/>
				</feMerge>
			</filter>
		</defs>

		<!-- Emergence entities along spiral -->
		{#each entities as v (v.id)}
			{@const transform = getTransform(v.progress, time)}
			{@const emergence = getEmergenceArms(transform.stage, transform.size)}
			<g
				transform="translate({transform.x}, {transform.y}) rotate({transform.rotation})"
				opacity={transform.opacity}
				class="emergence-group"
			>
				{#each emergence.arms as arm}
					<circle cx={0} cy={0} r={arm.circR} fill="none" class="emergence-stroke" stroke-width={emergence.sw} />
					<line x1={arm.ex} y1={arm.ey} x2={arm.tx} y2={arm.ty}
						class="emergence-stroke" stroke-width={emergence.sw} stroke-linecap="round" />
				{/each}
				{#if emergence.microArms}
					{#each emergence.microArms as micro}
						<g transform="translate({micro.parentX}, {micro.parentY})">
							<circle cx={0} cy={0} r={emergence.microCircR} fill="none" class="emergence-stroke" stroke-width={emergence.msw} />
							<line x1={micro.arm.ex} y1={micro.arm.ey} x2={micro.arm.tx} y2={micro.arm.ty}
								class="emergence-stroke" stroke-width={emergence.msw} stroke-linecap="round" />
						</g>
					{/each}
				{/if}
				{#each emergence.centers as c}
					<circle cx={0} cy={0} r={c.r} class="emergence-fill" opacity={0.35} />
				{/each}
			</g>
		{/each}

		<!-- Heptagon (constraint ring) -->
		<g class="heptagon" transform="translate({center}, {center}) rotate({heptagon.rotation})">
			<path d={heptagon.outline} fill="none" stroke-width={2} stroke-linejoin="round" opacity={0.85} />
			<path d={heptagon.star} fill="none" stroke-width={0.5} stroke-linejoin="round" opacity={0.2} />
			{#each heptagon.verts as v}
				<circle cx={v.x} cy={v.y} r={1.6} opacity={0.5} />
			{/each}
		</g>

		<!-- Spark (human agency) -->
		<g class="spark" filter="url(#spark-glow)">
			{#each sparkRays as ray}
				<line
					x1={center}
					y1={center}
					x2={ray.x2}
					y2={ray.y2}
					stroke-width={ray.width}
					stroke-linecap="round"
				/>
			{/each}
			<circle cx={center} cy={center} r={4} />
		</g>
	</svg>
</div>

<style>
	.sigil-container {
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100%;
	}

	.cage-line {
		position: absolute;
		background: oklch(62% 0.15 240 / 0.15);
	}

	.cage-line.north,
	.cage-line.south {
		left: 0;
		right: 0;
		height: 1px;
	}

	.cage-line.north { top: 0; }
	.cage-line.south { bottom: 0; }

	.cage-line.west,
	.cage-line.east {
		top: 0;
		bottom: 0;
		width: 1px;
	}

	.cage-line.west { left: 0; }
	.cage-line.east { right: 0; }

	.sigil {
		width: 100%;
		height: 100%;
		max-width: 100%;
		max-height: 100%;
		display: block;
		object-fit: contain;
	}

	.emergence-group {
		filter: url(#emergence-glow);
	}

	.emergence-stroke {
		stroke: var(--emergence-core);
	}

	.emergence-fill {
		fill: var(--emergence-core);
	}

	.heptagon path {
		stroke: var(--ci-red);
	}

	.heptagon circle {
		fill: var(--ci-red);
	}

	.spark line {
		stroke: var(--spark-core);
	}

	.spark circle {
		fill: var(--spark-core);
	}

	@media (prefers-reduced-motion: reduce) {
		.emergence-group {
			filter: none;
		}

		.spark {
			filter: none;
		}
	}
</style>
