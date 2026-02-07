<script lang="ts">
	import { T } from '@threlte/core';
</script>

<!-- Ambient for base visibility -->
<T.AmbientLight intensity={0.2} />

<!-- Blue point light from center (the spark illuminates) -->
<T.PointLight
	position={[0, 0, 0]}
	color="#00d4ff"
	intensity={4}
	distance={8}
/>

<!-- Subtle green rim light -->
<T.PointLight
	position={[3, 2, -2]}
	color="#00e8a0"
	intensity={0.8}
	distance={8}
/>

<!-- Red accent from the side -->
<T.PointLight
	position={[-2, -1, 2]}
	color="#ff3333"
	intensity={0.5}
	distance={6}
/>

<!-- Main key light -->
<T.DirectionalLight
	position={[5, 5, 5]}
	intensity={0.6}
/>
