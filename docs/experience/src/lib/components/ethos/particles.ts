/**
 * Ethos particle system — scroll-driven across 5 beats.
 * Canvas 2D. No WebGL. No dependencies.
 *
 * Narrative: foundations → shift → compounding → duty → invitation
 * Visual: sparse blue → red structure joins → green emergence flashes → upward convergence → settled balance
 */

import { smoothstep, lerp, type BeatState } from './beats';
import { getTrajectoryAttraction } from './trajectory';

// ─── Types ───

export interface Particle {
	id: number;
	x: number;
	y: number;
	vx: number;
	vy: number;
	baseColor: 'spark' | 'constraint' | 'ambient';
	radius: number;
	baseRadius: number;
	alpha: number;
	baseAlpha: number;
	chroma: number;
	baseChroma: number;
	hue: number;
	baseHue: number;
}

export interface Flash {
	x: number;
	y: number;
	birth: number;
}

// ─── Math utilities ───

function rand(min: number, max: number): number {
	return min + Math.random() * (max - min);
}

function dist(ax: number, ay: number, bx: number, by: number): number {
	const dx = ax - bx;
	const dy = ay - by;
	return Math.sqrt(dx * dx + dy * dy);
}

function easeOut(t: number): number {
	const c = Math.max(0, Math.min(1, t));
	return 1 - (1 - c) * (1 - c);
}

// ─── Colors ───

// OKLCH format — modern browsers support in canvas fillStyle
const VOID_HEX = '#050508';

function particleColor(p: Particle, alpha: number): string {
	const lightness = p.baseColor === 'spark' ? 75 : p.baseColor === 'constraint' ? 62 : 55;
	return `oklch(${lightness}% ${p.chroma.toFixed(3)} ${p.hue.toFixed(0)} / ${alpha.toFixed(3)})`;
}

// ─── Initialization ───

export function createParticles(w: number, h: number, mobile: boolean): Particle[] {
	const particles: Particle[] = [];
	const cx = w * 0.5;
	const cy = h * 0.5;
	const vw = w / 100;

	const sparkN = mobile ? 8 : 10;
	const constraintN = mobile ? 8 : 10;
	const ambientN = mobile ? 20 : 40;

	let id = 0;

	// Spark — blue, clustered at center, gentle upward bias
	for (let i = 0; i < sparkN; i++) {
		const a = Math.random() * Math.PI * 2;
		const d = rand(0, 8 * vw);
		const r = rand(2, 3.5);
		particles.push({
			id: id++,
			x: cx + Math.cos(a) * d,
			y: cy + Math.sin(a) * d,
			vx: rand(-0.01, 0.01) * vw,
			vy: rand(-0.015, 0.005) * vw, // slight upward bias
			baseColor: 'spark',
			radius: r,
			baseRadius: r,
			alpha: 0.85,
			baseAlpha: 0.85,
			chroma: 0.18,
			baseChroma: 0.18,
			hue: 240,
			baseHue: 240
		});
	}

	// Constraint — red, ring at 16-24vw from center
	for (let i = 0; i < constraintN; i++) {
		const a = (i / constraintN) * Math.PI * 2 + rand(-0.3, 0.3);
		const d = rand(16, 24) * vw;
		const r = rand(1.5, 2.5);
		particles.push({
			id: id++,
			x: cx + Math.cos(a) * d,
			y: cy + Math.sin(a) * d,
			vx: rand(-0.008, 0.008) * vw,
			vy: rand(-0.008, 0.008) * vw,
			baseColor: 'constraint',
			radius: r,
			baseRadius: r,
			alpha: 0,
			baseAlpha: 0.7,
			chroma: 0.2,
			baseChroma: 0.2,
			hue: 25,
			baseHue: 25
		});
	}

	// Ambient — scattered, near-grey, the field
	for (let i = 0; i < ambientN; i++) {
		const r = rand(1, 2);
		particles.push({
			id: id++,
			x: rand(0, w),
			y: rand(0, h),
			vx: rand(-0.012, 0.012) * vw,
			vy: rand(-0.012, 0.012) * vw,
			baseColor: 'ambient',
			radius: r,
			baseRadius: r,
			alpha: 0,
			baseAlpha: 0.35,
			chroma: 0.04,
			baseChroma: 0.04,
			hue: 240,
			baseHue: 240
		});
	}

	return particles;
}

// ─── Per-frame update ───

export function updateParticles(
	particles: Particle[],
	flashes: Flash[],
	state: BeatState,
	w: number,
	h: number,
	dt: number,
	now: number,
	mobile: boolean = false
): void {
	const cx = w * 0.5;
	const cy = h * 0.5;
	const vw = w / 100;
	const { beat, t } = state;

	for (const p of particles) {
		// Ambient drift (always)
		p.x += p.vx * dt;
		p.y += p.vy * dt;

		// Wrap edges with margin
		if (p.x < -20) p.x = w + 20;
		if (p.x > w + 20) p.x = -20;
		if (p.y < -20) p.y = h + 20;
		if (p.y > h + 20) p.y = -20;

		// ─── Beat 1: FOUNDATIONS — sparse, reverent ───
		// Sparks fade in from invisible — the reader discovers them.
		if (beat === 1) {
			if (p.baseColor === 'spark') {
				p.alpha = lerp(0, p.baseAlpha, smoothstep(t / 0.4));
				// Gentle upward drift
				p.vy -= 0.0001 * vw;
			} else if (p.baseColor === 'constraint') {
				// Invisible during foundations
				p.alpha = 0;
			} else {
				// Ambient: very faint at end of beat (transition to beat 2)
				p.alpha = lerp(0, 0.1, smoothstep((t - 0.7) / 0.3));
			}
		}

		// ─── Beat 2: THE SHIFT — red structure joins, field populates ───
		else if (beat === 2) {
			if (p.baseColor === 'spark') {
				p.alpha = p.baseAlpha;
				// Expand slightly — "we're all giants"
				p.radius = lerp(p.baseRadius, p.baseRadius * 1.4, smoothstep(t / 0.6));
			} else if (p.baseColor === 'constraint') {
				// Fade in, drift inward
				p.alpha = lerp(0, p.baseAlpha, smoothstep(t / 0.5));
				p.radius = lerp(p.baseRadius, p.baseRadius * 1.2, smoothstep(t / 0.6));
				// Pull toward center
				const dx = cx - p.x;
				const dy = cy - p.y;
				const d = Math.sqrt(dx * dx + dy * dy);
				if (d > 14 * vw) {
					p.vx += (dx / d) * 0.0008 * vw * smoothstep(t / 0.4);
					p.vy += (dy / d) * 0.0008 * vw * smoothstep(t / 0.4);
				}
			} else {
				// Ambient: populate the field
				p.alpha = lerp(0.1, p.baseAlpha, smoothstep(t / 0.5));
				p.radius = lerp(p.baseRadius, p.baseRadius * 1.3, smoothstep(t / 0.6));
			}
		}

		// ─── Beat 3: THE COMPOUNDING — all three alive, emergence flashes ───
		else if (beat === 3) {
			if (p.baseColor === 'spark') {
				p.alpha = lerp(p.baseAlpha, 1.0, smoothstep(t / 0.5));
				p.radius = lerp(p.baseRadius * 1.4, p.baseRadius * 1.6, smoothstep(t / 0.5));
			} else if (p.baseColor === 'constraint') {
				p.alpha = p.baseAlpha;
				// Ring tightens slightly
				const dx = cx - p.x;
				const dy = cy - p.y;
				const d = Math.sqrt(dx * dx + dy * dy);
				if (d > 10 * vw) {
					p.vx += (dx / d) * 0.0005 * vw;
					p.vy += (dy / d) * 0.0005 * vw;
				}
			} else {
				// Ambient: some shift toward blue or green
				p.alpha = p.baseAlpha * 1.5;
				if (p.id % 3 === 0) {
					p.hue = lerp(p.baseHue, 240, smoothstep(t / 0.6) * 0.5);
					p.chroma = lerp(p.baseChroma, 0.1, smoothstep(t / 0.6) * 0.4);
				} else if (p.id % 3 === 1) {
					p.hue = lerp(p.baseHue, 145, smoothstep(t / 0.6) * 0.3);
					p.chroma = lerp(p.baseChroma, 0.08, smoothstep(t / 0.6) * 0.3);
				}
			}

			// Emergence flashes — spark+constraint proximity
			if (flashes.length < 4) {
				// Proximity-based (organic)
				for (const s of particles) {
					if (s.baseColor !== 'spark') continue;
					for (const c of particles) {
						if (c.baseColor !== 'constraint' || c.alpha < 0.3) continue;
						if (dist(s.x, s.y, c.x, c.y) < 5 * vw && Math.random() < 0.01) {
							flashes.push({
								x: (s.x + c.x) / 2,
								y: (s.y + c.y) / 2,
								birth: now
							});
						}
					}
				}
				// Forced flashes in second half — reader must see emergence
				if (t > 0.5 && flashes.length < 2 && Math.random() < 0.015) {
					const s = particles.find((pp) => pp.baseColor === 'spark');
					const c = particles.find((pp) => pp.baseColor === 'constraint' && pp.alpha > 0.2);
					if (s && c) {
						flashes.push({
							x: (s.x + c.x) / 2,
							y: (s.y + c.y) / 2,
							birth: now
						});
					}
				}
			}
		}

		// ─── Beat 4: THE DUTY — upward structure, emergence dominant ───
		// Reduced upward force (gravity, not urgency). Constraint ring compresses.
		else if (beat === 4) {
			// Gentle upward drift (halved from before)
			const upwardForce = smoothstep(t / 0.6) * 0.0008 * vw;
			p.vy -= upwardForce;

			if (p.baseColor === 'spark') {
				p.alpha = lerp(1.0, 0.9, smoothstep(t / 0.5));
				p.radius = lerp(p.baseRadius * 1.6, p.baseRadius * 1.2, smoothstep(t / 0.5));
			} else if (p.baseColor === 'constraint') {
				p.alpha = lerp(p.baseAlpha, 0.6, smoothstep(t / 0.5));
				// Ring compresses — structure tightening around conviction
				const dx = cx - p.x;
				const dy = cy - p.y;
				const d = Math.sqrt(dx * dx + dy * dy);
				if (d > 8 * vw) {
					p.vx += (dx / d) * 0.0006 * vw * smoothstep(t / 0.5);
					p.vy += (dy / d) * 0.0006 * vw * smoothstep(t / 0.5);
				}
			} else {
				// Ambient shifts toward green (emergence)
				p.hue = lerp(p.hue, 145, smoothstep(t / 0.6) * 0.3);
				p.chroma = lerp(p.chroma, 0.12, smoothstep(t / 0.6) * 0.4);
				p.alpha = lerp(p.alpha, 0.5, smoothstep(t / 0.5) * 0.3);
			}

			// Trajectory attraction — particles cluster along their trajectory
			if (t > 0.5 && (p.baseColor === 'spark' || p.baseColor === 'constraint')) {
				const target = getTrajectoryAttraction(p.x, p.y, p.baseColor, w, h, mobile);
				if (target) {
					const dx = target.tx - p.x;
					const dy = target.ty - p.y;
					const d = Math.sqrt(dx * dx + dy * dy);
					if (d > 1) {
						const force = (mobile ? 0.00015 : 0.0003) * vw * smoothstep((t - 0.5) / 0.3);
						p.vx += (dx / d) * force;
						p.vy += (dy / d) * force;
					}
				}
			}

			// Steady emergence flashes
			if (flashes.length < 3 && Math.random() < 0.006) {
				const s = particles.find((pp) => pp.baseColor === 'spark' && pp.alpha > 0.5);
				const c = particles.find((pp) => pp.baseColor === 'constraint' && pp.alpha > 0.3);
				if (s && c && dist(s.x, s.y, c.x, c.y) < 8 * vw) {
					flashes.push({ x: (s.x + c.x) / 2, y: (s.y + c.y) / 2, birth: now });
				}
			}
		}

		// ─── Beat 5: THE INVITATION — settle, colors balance ───
		// Stronger decay — the field comes to rest.
		else if (beat === 5) {
			// Velocity decays firmly
			p.vx *= 1 - 0.008 * smoothstep(t / 0.4);
			p.vy *= 1 - 0.008 * smoothstep(t / 0.4);

			// Restore base colors
			const settle = smoothstep(t / 0.6);
			p.chroma = lerp(p.chroma, p.baseChroma, settle * 0.4);
			p.hue = lerp(p.hue, p.baseHue, settle * 0.4);
			p.radius = lerp(p.radius, p.baseRadius, settle * 0.3);

			if (p.baseColor === 'spark') p.alpha = lerp(p.alpha, 0.8, settle * 0.3);
			else if (p.baseColor === 'constraint') p.alpha = lerp(p.alpha, 0.5, settle * 0.3);
			else p.alpha = lerp(p.alpha, 0.4, settle * 0.3);

			// Occasional slow flashes
			if (flashes.length < 2 && Math.random() < 0.003) {
				const s = particles.find((pp) => pp.baseColor === 'spark');
				const c = particles.find((pp) => pp.baseColor === 'constraint');
				if (s && c && dist(s.x, s.y, c.x, c.y) < 10 * vw) {
					flashes.push({ x: (s.x + c.x) / 2, y: (s.y + c.y) / 2, birth: now });
				}
			}
		}

		// Velocity cap
		const speed = Math.sqrt(p.vx * p.vx + p.vy * p.vy);
		const maxSpeed = 0.05 * vw;
		if (speed > maxSpeed) {
			p.vx = (p.vx / speed) * maxSpeed;
			p.vy = (p.vy / speed) * maxSpeed;
		}
	}

	// Clean expired flashes
	const FLASH_DURATION = 450;
	for (let i = flashes.length - 1; i >= 0; i--) {
		if (now - flashes[i].birth > FLASH_DURATION) flashes.splice(i, 1);
	}
}

// ─── Rendering ───

export function render(
	ctx: CanvasRenderingContext2D,
	particles: Particle[],
	flashes: Flash[],
	w: number,
	h: number,
	dpr: number,
	now: number
): void {
	// Clear with void
	ctx.fillStyle = VOID_HEX;
	ctx.fillRect(0, 0, w * dpr, h * dpr);

	ctx.save();
	ctx.scale(dpr, dpr);

	// Particles
	for (const p of particles) {
		if (p.alpha < 0.01) continue;

		const color = particleColor(p, p.alpha);

		// Halo — soft glow around each particle
		const haloR = p.radius * 2.5;
		const grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, haloR);
		grad.addColorStop(0, particleColor(p, p.alpha * 0.15));
		grad.addColorStop(1, 'transparent');
		ctx.fillStyle = grad;
		ctx.beginPath();
		ctx.arc(p.x, p.y, haloR, 0, Math.PI * 2);
		ctx.fill();

		// Core
		ctx.fillStyle = color;
		ctx.beginPath();
		ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
		ctx.fill();
	}

	// Emergence flashes (green)
	const FLASH_DURATION = 450;
	for (const f of flashes) {
		const age = (now - f.birth) / FLASH_DURATION;
		if (age > 1) continue;
		const a = easeOut(1 - age) * 0.85;
		const r = lerp(3, 5, easeOut(age));
		ctx.fillStyle = `oklch(75% 0.18 145 / ${a.toFixed(3)})`;
		ctx.beginPath();
		ctx.arc(f.x, f.y, r, 0, Math.PI * 2);
		ctx.fill();
	}

	ctx.restore();
}
