<script lang="ts">
	// 2D animated dialectical glyph using SVG + CSS
	// Blue spark (human) → Red ring (machine) → Green emergence (gestalt)
</script>

<div class="glyph-container">
	<svg viewBox="-200 -200 400 400" class="glyph">
		<!-- Definitions for gradients and filters -->
		<defs>
			<!-- Blue spark glow -->
			<filter id="spark-glow" x="-50%" y="-50%" width="200%" height="200%">
				<feGaussianBlur stdDeviation="4" result="blur" />
				<feMerge>
					<feMergeNode in="blur" />
					<feMergeNode in="SourceGraphic" />
				</feMerge>
			</filter>

			<!-- Red ring glow -->
			<filter id="ring-glow" x="-50%" y="-50%" width="200%" height="200%">
				<feGaussianBlur stdDeviation="2" result="blur" />
				<feMerge>
					<feMergeNode in="blur" />
					<feMergeNode in="SourceGraphic" />
				</feMerge>
			</filter>

			<!-- Green emergence glow -->
			<filter id="emergence-glow" x="-50%" y="-50%" width="200%" height="200%">
				<feGaussianBlur stdDeviation="3" result="blur" />
				<feMerge>
					<feMergeNode in="blur" />
					<feMergeNode in="SourceGraphic" />
				</feMerge>
			</filter>

			<!-- Radial gradient for spark -->
			<radialGradient id="spark-gradient">
				<stop offset="0%" stop-color="#00d4ff" stop-opacity="1" />
				<stop offset="50%" stop-color="#00d4ff" stop-opacity="0.5" />
				<stop offset="100%" stop-color="#00d4ff" stop-opacity="0" />
			</radialGradient>
		</defs>

		<!-- Green Emergence: Structures at cardinal points -->
		<g class="emergence-layer">
			<!-- North: Simple diamond -->
			<g class="emergence" transform="translate(0, -100)">
				<g class="float-n">
					<polygon
						points="0,-10 8,0 0,10 -8,0"
						fill="none"
						stroke="#00e8a0"
						stroke-width="2"
						filter="url(#emergence-glow)"
					/>
				</g>
			</g>

			<!-- East: Two shapes -->
			<g class="emergence" transform="translate(120, 0)">
				<g class="float-e">
					<polygon
						points="0,-12 9,0 0,12 -9,0"
						fill="#00e8a0"
						fill-opacity="0.3"
						stroke="#00e8a0"
						stroke-width="2"
						filter="url(#emergence-glow)"
					/>
					<polygon
						points="20,-6 26,0 20,6 14,0"
						fill="none"
						stroke="#00e8a0"
						stroke-width="1.5"
						opacity="0.7"
					/>
				</g>
			</g>

			<!-- South: Three shapes -->
			<g class="emergence" transform="translate(0, 130)">
				<g class="float-s">
					<polygon
						points="0,-14 12,7 -12,7"
						fill="#00e8a0"
						fill-opacity="0.4"
						stroke="#00e8a0"
						stroke-width="2"
						filter="url(#emergence-glow)"
					/>
					<polygon
						points="-18,10 -12,20 -24,20"
						fill="none"
						stroke="#00e8a0"
						stroke-width="1.5"
						opacity="0.6"
					/>
					<polygon
						points="18,10 24,20 12,20"
						fill="none"
						stroke="#00e8a0"
						stroke-width="1.5"
						opacity="0.6"
					/>
				</g>
			</g>

			<!-- West: Four shapes (full mastery) -->
			<g class="emergence" transform="translate(-130, 0)">
				<g class="float-w">
					<!-- Outer wireframe hexagon -->
					<polygon
						points="0,-22 19,-11 19,11 0,22 -19,11 -19,-11"
						fill="none"
						stroke="#00e8a0"
						stroke-width="1.5"
						opacity="0.5"
						class="hex-spin"
					/>
					<!-- Inner solid -->
					<polygon
						points="0,-12 10,-6 10,6 0,12 -10,6 -10,-6"
						fill="#00e8a0"
						fill-opacity="0.5"
						stroke="#00e8a0"
						stroke-width="2"
						filter="url(#emergence-glow)"
					/>
					<!-- Orbiting dots -->
					<g class="orbit-group">
						<circle cx="0" cy="-30" r="4" fill="#00e8a0" opacity="0.8" />
					</g>
					<g class="orbit-group delay-1">
						<circle cx="0" cy="-30" r="3" fill="#00e8a0" opacity="0.6" />
					</g>
					<g class="orbit-group delay-2">
						<circle cx="0" cy="-30" r="2.5" fill="#00e8a0" opacity="0.7" />
					</g>
				</g>
			</g>
		</g>

		<!-- Red Containment Ring -->
		<g class="ring-layer">
			<ellipse
				cx="0"
				cy="0"
				rx="70"
				ry="25"
				fill="none"
				stroke="#ff3333"
				stroke-width="8"
				stroke-linecap="round"
				filter="url(#ring-glow)"
				class="ring"
			/>
			<!-- Mechanical segments on ring -->
			<g class="ring-segments">
				<rect x="65" y="-6" width="12" height="12" fill="#ff3333" opacity="0.8" />
				<rect x="-77" y="-6" width="12" height="12" fill="#ff3333" opacity="0.8" />
			</g>
		</g>

		<!-- Blue Spark: Human spirit at center -->
		<g class="spark-layer">
			<!-- Outer glow -->
			<circle
				cx="0"
				cy="0"
				r="35"
				fill="url(#spark-gradient)"
				class="spark-atmosphere"
			/>

			<!-- Spark rays -->
			<g class="spark-rays">
				{#each [0, 45, 90, 135, 180, 225, 270, 315] as angle}
					<line
						x1="0"
						y1="0"
						x2={Math.cos(angle * Math.PI / 180) * 28}
						y2={Math.sin(angle * Math.PI / 180) * 28}
						stroke="#00d4ff"
						stroke-width="2"
						stroke-linecap="round"
						opacity="0.7"
					/>
				{/each}
			</g>

			<!-- Core spark -->
			<circle
				cx="0"
				cy="0"
				r="12"
				fill="#00d4ff"
				filter="url(#spark-glow)"
				class="spark-core"
			/>
		</g>
	</svg>
</div>

<style>
	.glyph-container {
		position: fixed;
		inset: 0;
		z-index: -1;
		display: flex;
		align-items: center;
		justify-content: center;
		padding-bottom: 15vh; /* Offset to position glyph above text */
	}

	.glyph {
		width: min(80vw, 500px);
		height: auto;
	}

	/* Blue spark animations */
	.spark-core {
		animation: pulse 2s ease-in-out infinite;
	}

	.spark-atmosphere {
		animation: breathe 3s ease-in-out infinite;
	}

	.spark-rays {
		animation: ray-pulse 2s ease-in-out infinite;
	}

	@keyframes pulse {
		0%, 100% { opacity: 1; transform: scale(1); }
		50% { opacity: 0.85; transform: scale(1.1); }
	}

	@keyframes breathe {
		0%, 100% { opacity: 0.6; transform: scale(1); }
		50% { opacity: 0.8; transform: scale(1.15); }
	}

	@keyframes ray-pulse {
		0%, 100% { opacity: 0.7; }
		50% { opacity: 0.9; }
	}

	/* Red ring animation */
	.ring-layer {
		animation: ring-rotate 20s linear infinite;
	}

	@keyframes ring-rotate {
		from { transform: rotateX(60deg) rotateZ(0deg); }
		to { transform: rotateX(60deg) rotateZ(360deg); }
	}

	/* Green emergence animations */
	.emergence-layer {
		animation: emergence-orbit 40s linear infinite reverse;
	}

	.float-n {
		animation: float 4s ease-in-out infinite;
	}

	.float-e {
		animation: float 3.5s ease-in-out infinite 0.5s;
	}

	.float-s {
		animation: float 4.5s ease-in-out infinite 1s;
	}

	.float-w {
		animation: float 3s ease-in-out infinite 0.25s;
	}

	.hex-spin {
		animation: spin 12s linear infinite;
		transform-origin: center;
	}

	.orbit-group {
		animation: orbit 5s linear infinite;
		transform-origin: center;
	}

	.orbit-group.delay-1 {
		animation-delay: -1.66s;
	}

	.orbit-group.delay-2 {
		animation-delay: -3.33s;
	}

	@keyframes float {
		0%, 100% { transform: translateY(0); }
		50% { transform: translateY(-6px); }
	}

	@keyframes spin {
		from { transform: rotate(0deg); }
		to { transform: rotate(360deg); }
	}

	@keyframes orbit {
		from { transform: rotate(0deg); }
		to { transform: rotate(360deg); }
	}

	@keyframes emergence-orbit {
		from { transform: rotate(0deg); }
		to { transform: rotate(360deg); }
	}

	/* Reduced motion */
	@media (prefers-reduced-motion: reduce) {
		.spark-core,
		.spark-atmosphere,
		.spark-rays,
		.ring-layer,
		.emergence-layer,
		.emergence-n,
		.emergence-e,
		.emergence-s,
		.emergence-w,
		.hex-outer,
		.orbit-dot {
			animation: none;
		}
	}
</style>
