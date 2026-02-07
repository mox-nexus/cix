<script lang="ts">
	import { Canvas, T } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';
	import DialecticalGlyph from './DialecticalGlyph.svelte';
	import GlyphLighting from './GlyphLighting.svelte';
</script>

<div class="glyph-container">
	<Canvas>
		<!-- Camera positioned to show glyph in upper-center of viewport -->
		<T.PerspectiveCamera makeDefault position={[0, -1.2, 5.5]} fov={45}>
			<OrbitControls
				enableZoom={false}
				enablePan={false}
				autoRotate
				autoRotateSpeed={0.25}
				maxPolarAngle={Math.PI / 1.6}
				minPolarAngle={Math.PI / 2.8}
			/>
		</T.PerspectiveCamera>

		<!-- Lighting -->
		<GlyphLighting />

		<!-- The dialectical glyph -->
		<DialecticalGlyph />
	</Canvas>
</div>

<style>
	.glyph-container {
		position: fixed;
		inset: 0;
		z-index: -1;
	}
</style>
