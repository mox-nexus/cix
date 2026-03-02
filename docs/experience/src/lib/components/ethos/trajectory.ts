/**
 * Trajectory field — the dominant visual object that transforms across all 5 beats.
 *
 * Beat 1: Seed point + single rising path (inheritance)
 * Beat 2: Multiple converging paths + convergence pulse (giants meeting)
 * Beat 3: Path steepens, velocity ticks appear (acceleration)
 * Beat 4: Path forks — rising (green) and declining (red) (the divergence)
 * Beat 5: Fork ghosts out, new single rising line (the foundation)
 *
 * All coordinates expressed as fractions of viewport (w, h).
 * Canvas 2D only. No dependencies.
 */

import { smoothstep, lerp, type BeatState } from './beats';

// ─── Geometry constants ───

interface TrajectoryGeometry {
	// Origin (seed point, bottom of rising path)
	ox: number;
	oy: number;
	// Convergence point (where histories meet, fork begins)
	cx: number;
	cy: number;
	// Rising future (green)
	riseCtrlX: number;
	riseCtrlY: number;
	riseEndX: number;
	riseEndY: number;
	// Declining future (red)
	fallCtrlX: number;
	fallCtrlY: number;
	fallEndX: number;
	fallEndY: number;
}

function getGeometry(w: number, h: number, mobile: boolean): TrajectoryGeometry {
	if (mobile) {
		return {
			ox: w * 0.5,
			oy: h * 0.55,
			cx: w * 0.5,
			cy: h * 0.35,
			riseCtrlX: w * 0.6,
			riseCtrlY: h * 0.22,
			riseEndX: w * 0.75,
			riseEndY: h * 0.1,
			fallCtrlX: w * 0.6,
			fallCtrlY: h * 0.42,
			fallEndX: w * 0.75,
			fallEndY: h * 0.55
		};
	}
	return {
		ox: w * 0.5,
		oy: h * 0.65,
		cx: w * 0.5,
		cy: h * 0.38,
		riseCtrlX: w * 0.55,
		riseCtrlY: h * 0.25,
		riseEndX: w * 0.65,
		riseEndY: h * 0.12,
		fallCtrlX: w * 0.55,
		fallCtrlY: h * 0.42,
		fallEndX: w * 0.7,
		fallEndY: h * 0.52
	};
}

// ─── Bezier utilities ───

function bezierPoint(
	x0: number,
	y0: number,
	cx: number,
	cy: number,
	x1: number,
	y1: number,
	t: number
): [number, number] {
	const mt = 1 - t;
	return [mt * mt * x0 + 2 * mt * t * cx + t * t * x1, mt * mt * y0 + 2 * mt * t * cy + t * t * y1];
}

function drawBezierProgress(
	ctx: CanvasRenderingContext2D,
	x0: number,
	y0: number,
	cx: number,
	cy: number,
	x1: number,
	y1: number,
	progress: number
): void {
	const SEGMENTS = 40;
	const maxSeg = Math.max(1, Math.floor(progress * SEGMENTS));
	ctx.moveTo(x0, y0);
	for (let i = 1; i <= maxSeg; i++) {
		const t = i / SEGMENTS;
		const [bx, by] = bezierPoint(x0, y0, cx, cy, x1, y1, t);
		ctx.lineTo(bx, by);
	}
}

// ─── Beat 1: Seed + single rising path ───

function drawBeat1(
	ctx: CanvasRenderingContext2D,
	geo: TrajectoryGeometry,
	t: number
): void {
	// Seed point — appears at t > 0.1
	const seedAlpha = smoothstep((t - 0.1) / 0.3) * 0.4;
	if (seedAlpha > 0.01) {
		ctx.fillStyle = `oklch(75% 0.18 240 / ${seedAlpha.toFixed(3)})`;
		ctx.beginPath();
		ctx.arc(geo.ox, geo.oy, 3, 0, Math.PI * 2);
		ctx.fill();
	}

	// Rising path draws from origin toward convergence
	const pathProgress = smoothstep((t - 0.2) / 0.7);
	if (pathProgress > 0.02) {
		const pathAlpha = smoothstep((t - 0.2) / 0.4) * 0.2;
		ctx.save();
		ctx.strokeStyle = `oklch(75% 0.18 240 / ${pathAlpha.toFixed(3)})`;
		ctx.lineWidth = 1;
		ctx.lineCap = 'round';
		ctx.beginPath();
		drawBezierProgress(
			ctx,
			geo.ox,
			geo.oy,
			(geo.ox + geo.cx) / 2,
			(geo.oy + geo.cy) / 2,
			geo.cx,
			geo.cy,
			pathProgress
		);
		ctx.stroke();
		ctx.restore();
	}
}

// ─── Beat 2: Multiple converging paths + pulse ───

function drawBeat2(
	ctx: CanvasRenderingContext2D,
	geo: TrajectoryGeometry,
	w: number,
	h: number,
	t: number,
	mobile: boolean,
	now: number
): void {
	const pathCount = mobile ? 3 : 5;
	const pathAlpha = lerp(0.2, 0.15, smoothstep(t / 0.5));

	// Multiple origin points that converge at cx, cy
	const offsets = mobile
		? [
				[-w * 0.15, h * 0.12],
				[0, 0],
				[w * 0.15, h * 0.12]
			]
		: [
				[-w * 0.2, h * 0.15],
				[-w * 0.1, h * 0.08],
				[0, 0],
				[w * 0.1, h * 0.08],
				[w * 0.2, h * 0.15]
			];

	const arriveProgress = smoothstep(t / 0.6);

	for (let i = 0; i < pathCount; i++) {
		const [dx, dy] = offsets[i];
		const startX = geo.ox + dx;
		const startY = geo.oy + dy;
		// Each path arrives at a slightly staggered time
		const delay = i * 0.05;
		const progress = smoothstep((t - delay) / 0.6);
		if (progress < 0.02) continue;

		const alpha = pathAlpha * progress;
		ctx.save();
		ctx.strokeStyle = `oklch(75% 0.18 240 / ${alpha.toFixed(3)})`;
		ctx.lineWidth = 1;
		ctx.lineCap = 'round';
		ctx.beginPath();
		drawBezierProgress(
			ctx,
			startX,
			startY,
			(startX + geo.cx) / 2,
			(startY + geo.cy) / 2,
			geo.cx,
			geo.cy,
			progress
		);
		ctx.stroke();
		ctx.restore();
	}

	// Convergence pulse — radial ripple at the meeting point
	if (arriveProgress > 0.3) {
		const pulsePhase = ((now % 800) / 800) * Math.PI * 2;
		const pulseR = 6 + Math.sin(pulsePhase) * 4;
		const pulseAlpha = 0.12 * smoothstep((arriveProgress - 0.3) / 0.3);
		ctx.save();
		ctx.strokeStyle = `oklch(75% 0.18 240 / ${pulseAlpha.toFixed(3)})`;
		ctx.lineWidth = 1.5;
		ctx.beginPath();
		ctx.arc(geo.cx, geo.cy, pulseR, 0, Math.PI * 2);
		ctx.stroke();
		ctx.restore();
	}
}

// ─── Beat 3: Path steepens + velocity ticks ───

function drawBeat3(
	ctx: CanvasRenderingContext2D,
	geo: TrajectoryGeometry,
	t: number,
	mobile: boolean
): void {
	// The merged upward path continues from convergence and steepens
	// Control point moves upward as t increases, changing curve shape
	const steepen = smoothstep(t / 0.7);
	const pathAlpha = lerp(0.2, 0.4, steepen);
	const lineW = lerp(1, 1.5, steepen);

	// Rising continuation from convergence to above
	const risingCtrlX = geo.cx - geo.cx * 0.05 * steepen;
	const risingCtrlY = geo.cy - (geo.cy * 0.3 + geo.cy * 0.15 * steepen);
	const risingEndX = geo.cx;
	const risingEndY = Math.max(0, geo.cy - geo.cy * 0.5 * (1 + steepen * 0.5));

	const progress = smoothstep(t / 0.8);

	ctx.save();
	ctx.strokeStyle = `oklch(75% 0.18 240 / ${pathAlpha.toFixed(3)})`;
	ctx.lineWidth = lineW;
	ctx.lineCap = 'round';
	ctx.beginPath();
	drawBezierProgress(ctx, geo.cx, geo.cy, risingCtrlX, risingCtrlY, risingEndX, risingEndY, progress);
	ctx.stroke();

	// Also draw the inherited path from origin to convergence (fading context)
	ctx.strokeStyle = `oklch(75% 0.18 240 / ${(pathAlpha * 0.5).toFixed(3)})`;
	ctx.lineWidth = 1;
	ctx.beginPath();
	drawBezierProgress(
		ctx,
		geo.ox,
		geo.oy,
		(geo.ox + geo.cx) / 2,
		(geo.oy + geo.cy) / 2,
		geo.cx,
		geo.cy,
		1
	);
	ctx.stroke();

	// Velocity ticks — perpendicular marks that get closer together
	if (!mobile && progress > 0.3) {
		const tickPositions = [0.3, 0.6, 0.85];
		for (const tp of tickPositions) {
			if (progress < tp) continue;
			const tickAlpha = smoothstep((progress - tp) / 0.15) * 0.25;
			const [px, py] = bezierPoint(
				geo.cx,
				geo.cy,
				risingCtrlX,
				risingCtrlY,
				risingEndX,
				risingEndY,
				tp
			);
			ctx.strokeStyle = `oklch(75% 0.12 240 / ${tickAlpha.toFixed(3)})`;
			ctx.lineWidth = 1;
			ctx.beginPath();
			ctx.moveTo(px - 4, py);
			ctx.lineTo(px + 4, py);
			ctx.stroke();
		}
	}

	ctx.restore();
}

// ─── Beat 4: The Fork ───

function drawBeat4(
	ctx: CanvasRenderingContext2D,
	geo: TrajectoryGeometry,
	t: number,
	mobile: boolean
): void {
	// Inherited path — origin to convergence (fading)
	const inheritAlpha = lerp(0.2, 0.1, smoothstep(t / 0.5));
	ctx.save();
	ctx.strokeStyle = `oklch(75% 0.18 240 / ${inheritAlpha.toFixed(3)})`;
	ctx.lineWidth = 1;
	ctx.lineCap = 'round';
	ctx.beginPath();
	drawBezierProgress(
		ctx,
		geo.ox,
		geo.oy,
		(geo.ox + geo.cx) / 2,
		(geo.oy + geo.cy) / 2,
		geo.cx,
		geo.cy,
		1
	);
	ctx.stroke();
	ctx.restore();

	// Phase 1 (t < 0.15): single path, no fork visible
	// Phase 2 (0.15 < t < 0.5): blur at convergence — probability cloud
	if (t > 0.15 && t < 0.5) {
		const blur = smoothstep((t - 0.15) / 0.35);
		ctx.save();
		ctx.strokeStyle = `oklch(68% 0.12 200 / ${(0.12 * blur).toFixed(3)})`;
		ctx.lineWidth = 2 + blur * 1.5;
		ctx.beginPath();
		ctx.arc(geo.cx, geo.cy, 6 + blur * 4, 0, Math.PI * 2);
		ctx.stroke();
		ctx.restore();
	}

	// Phase 3 (t > 0.5): diverging trajectories draw themselves
	if (t > 0.5) {
		const drawT = smoothstep((t - 0.5) / 0.35);

		// Rising trajectory — emergence green
		const riseAlpha = drawT * 0.6;
		ctx.save();
		ctx.strokeStyle = `oklch(72% 0.16 145 / ${riseAlpha.toFixed(3)})`;
		ctx.lineWidth = mobile ? 1 : 1.5 + drawT * 0.5;
		ctx.lineCap = 'round';
		ctx.beginPath();
		drawBezierProgress(
			ctx,
			geo.cx,
			geo.cy,
			geo.riseCtrlX,
			geo.riseCtrlY,
			geo.riseEndX,
			geo.riseEndY,
			drawT
		);
		ctx.stroke();
		ctx.restore();

		// Declining trajectory — constraint red (thins as it draws)
		const fallAlpha = drawT * 0.4;
		ctx.save();
		ctx.strokeStyle = `oklch(58% 0.18 25 / ${fallAlpha.toFixed(3)})`;
		ctx.lineWidth = mobile ? 0.75 : Math.max(0.5, 1.5 - drawT * 0.5);
		ctx.lineCap = 'round';
		ctx.beginPath();
		drawBezierProgress(
			ctx,
			geo.cx,
			geo.cy,
			geo.fallCtrlX,
			geo.fallCtrlY,
			geo.fallEndX,
			geo.fallEndY,
			drawT
		);
		ctx.stroke();
		ctx.restore();
	}

	// Fork point — white dot of indetermination
	if (t > 0.15 && t < 0.85) {
		const dotAlpha = t < 0.5 ? smoothstep((t - 0.15) / 0.2) * 0.15 : lerp(0.15, 0, smoothstep((t - 0.5) / 0.35));
		ctx.save();
		ctx.fillStyle = `oklch(90% 0 0 / ${dotAlpha.toFixed(3)})`;
		ctx.beginPath();
		ctx.arc(geo.cx, geo.cy, 4, 0, Math.PI * 2);
		ctx.fill();
		ctx.restore();
	}
}

// ─── Beat 5: Ghost out + new foundation line ───

function drawBeat5(
	ctx: CanvasRenderingContext2D,
	geo: TrajectoryGeometry,
	t: number,
	mobile: boolean
): void {
	// Ghost the fork trajectories
	const ghostAlpha = lerp(0.3, 0.03, smoothstep(t / 0.5));
	if (ghostAlpha > 0.02) {
		// Rising ghost
		ctx.save();
		ctx.strokeStyle = `oklch(72% 0.16 145 / ${(ghostAlpha * 0.6).toFixed(3)})`;
		ctx.lineWidth = mobile ? 0.75 : 1;
		ctx.lineCap = 'round';
		ctx.beginPath();
		drawBezierProgress(
			ctx,
			geo.cx,
			geo.cy,
			geo.riseCtrlX,
			geo.riseCtrlY,
			geo.riseEndX,
			geo.riseEndY,
			1
		);
		ctx.stroke();
		ctx.restore();

		// Declining ghost
		ctx.save();
		ctx.strokeStyle = `oklch(58% 0.18 25 / ${(ghostAlpha * 0.3).toFixed(3)})`;
		ctx.lineWidth = mobile ? 0.5 : 0.75;
		ctx.lineCap = 'round';
		ctx.beginPath();
		drawBezierProgress(
			ctx,
			geo.cx,
			geo.cy,
			geo.fallCtrlX,
			geo.fallCtrlY,
			geo.fallEndX,
			geo.fallEndY,
			1
		);
		ctx.stroke();
		ctx.restore();
	}

	// New single rising line — the foundation being laid
	// Gradient from spark blue (bottom) to emergence green (top)
	const riseProgress = smoothstep((t - 0.2) / 0.5);
	if (riseProgress > 0.02) {
		const riseAlpha = riseProgress * 0.3;
		// Simple line from below center to above
		const startX = geo.cx;
		const startY = geo.cy + (geo.oy - geo.cy) * 0.3;
		const endX = geo.cx;
		const endY = geo.cy - (geo.cy * 0.3);
		const ctrlX = geo.cx - geo.cx * 0.03;
		const ctrlY = (startY + endY) / 2;

		// Draw with gradient — spark blue at bottom, emergence green at top
		const grad = ctx.createLinearGradient(startX, startY, endX, endY);
		grad.addColorStop(0, `oklch(75% 0.18 240 / ${riseAlpha.toFixed(3)})`);
		grad.addColorStop(1, `oklch(72% 0.16 145 / ${riseAlpha.toFixed(3)})`);

		ctx.save();
		ctx.strokeStyle = grad;
		ctx.lineWidth = mobile ? 1 : 1.5;
		ctx.lineCap = 'round';
		ctx.beginPath();
		drawBezierProgress(ctx, startX, startY, ctrlX, ctrlY, endX, endY, riseProgress);
		ctx.stroke();
		ctx.restore();
	}
}

// ─── Public API ───

export function drawTrajectories(
	ctx: CanvasRenderingContext2D,
	state: BeatState,
	w: number,
	h: number,
	mobile: boolean,
	now: number
): void {
	const geo = getGeometry(w, h, mobile);
	const { beat, t } = state;

	switch (beat) {
		case 1:
			drawBeat1(ctx, geo, t);
			break;
		case 2:
			drawBeat2(ctx, geo, w, h, t, mobile, now);
			break;
		case 3:
			drawBeat3(ctx, geo, t, mobile);
			break;
		case 4:
			drawBeat4(ctx, geo, t, mobile);
			break;
		case 5:
			drawBeat5(ctx, geo, t, mobile);
			break;
	}
}

/**
 * Static render for reduced motion — shows the full fork at Beat 4 completion.
 */
export function drawTrajectoriesStatic(
	ctx: CanvasRenderingContext2D,
	w: number,
	h: number,
	mobile: boolean
): void {
	const geo = getGeometry(w, h, mobile);

	// Draw inherited path
	ctx.save();
	ctx.strokeStyle = 'oklch(75% 0.18 240 / 0.15)';
	ctx.lineWidth = 1;
	ctx.lineCap = 'round';
	ctx.beginPath();
	drawBezierProgress(
		ctx,
		geo.ox,
		geo.oy,
		(geo.ox + geo.cx) / 2,
		(geo.oy + geo.cy) / 2,
		geo.cx,
		geo.cy,
		1
	);
	ctx.stroke();
	ctx.restore();

	// Rising trajectory — full
	ctx.save();
	ctx.strokeStyle = 'oklch(72% 0.16 145 / 0.5)';
	ctx.lineWidth = mobile ? 1 : 1.5;
	ctx.lineCap = 'round';
	ctx.beginPath();
	drawBezierProgress(
		ctx,
		geo.cx,
		geo.cy,
		geo.riseCtrlX,
		geo.riseCtrlY,
		geo.riseEndX,
		geo.riseEndY,
		1
	);
	ctx.stroke();
	ctx.restore();

	// Declining trajectory — full
	ctx.save();
	ctx.strokeStyle = 'oklch(58% 0.18 25 / 0.35)';
	ctx.lineWidth = mobile ? 0.75 : 1;
	ctx.lineCap = 'round';
	ctx.beginPath();
	drawBezierProgress(
		ctx,
		geo.cx,
		geo.cy,
		geo.fallCtrlX,
		geo.fallCtrlY,
		geo.fallEndX,
		geo.fallEndY,
		1
	);
	ctx.stroke();
	ctx.restore();
}

/**
 * Get the closest point on the rising/declining trajectory for particle attraction.
 * Returns the target point and which trajectory it belongs to.
 */
export function getTrajectoryAttraction(
	px: number,
	py: number,
	particleType: 'spark' | 'constraint',
	w: number,
	h: number,
	mobile: boolean
): { tx: number; ty: number } | null {
	const geo = getGeometry(w, h, mobile);

	// Spark particles attracted to rising (green), constraint to declining (red)
	if (particleType === 'spark') {
		// Sample a few points on the rising trajectory, find closest
		let bestD = Infinity;
		let bestX = 0;
		let bestY = 0;
		for (let i = 0; i <= 8; i++) {
			const t = i / 8;
			const [bx, by] = bezierPoint(
				geo.cx,
				geo.cy,
				geo.riseCtrlX,
				geo.riseCtrlY,
				geo.riseEndX,
				geo.riseEndY,
				t
			);
			const dx = px - bx;
			const dy = py - by;
			const d = dx * dx + dy * dy;
			if (d < bestD) {
				bestD = d;
				bestX = bx;
				bestY = by;
			}
		}
		return { tx: bestX, ty: bestY };
	} else {
		let bestD = Infinity;
		let bestX = 0;
		let bestY = 0;
		for (let i = 0; i <= 8; i++) {
			const t = i / 8;
			const [bx, by] = bezierPoint(
				geo.cx,
				geo.cy,
				geo.fallCtrlX,
				geo.fallCtrlY,
				geo.fallEndX,
				geo.fallEndY,
				t
			);
			const dx = px - bx;
			const dy = py - by;
			const d = dx * dx + dy * dy;
			if (d < bestD) {
				bestD = d;
				bestX = bx;
				bestY = by;
			}
		}
		return { tx: bestX, ty: bestY };
	}
}
