<script lang="ts">
	import { T, useTask } from '@threlte/core';
	import { Float } from '@threlte/extras';
	import * as THREE from 'three';

	// Animation state
	let time = $state(0);

	useTask((delta) => {
		time += delta;
	});

	// Colors from the dialectical system
	const BLUE_SPARK = new THREE.Color('#00d4ff');
	const RED_CONTAINMENT = new THREE.Color('#ff3333');
	const GREEN_EMERGENCE = new THREE.Color('#00e8a0');

	// Derived animations
	let sparkPulse = $derived(0.8 + Math.sin(time * 2) * 0.2);
	let ringRotation = $derived(time * 0.3);
	let emergenceRotation = $derived(time * 0.15);
</script>

<!-- Blue Spark: Human spirit at center -->
<T.Group>
	<!-- Core glow - larger, more prominent -->
	<T.Mesh>
		<T.SphereGeometry args={[0.2, 32, 32]} />
		<T.MeshBasicMaterial color={BLUE_SPARK} transparent opacity={sparkPulse} />
	</T.Mesh>

	<!-- Inner spark rays - 8 rays for balance -->
	{#each [0, 45, 90, 135, 180, 225, 270, 315] as angle}
		<T.Mesh rotation.z={THREE.MathUtils.degToRad(angle)}>
			<T.CylinderGeometry args={[0.025, 0.008, 0.5, 8]} />
			<T.MeshBasicMaterial color={BLUE_SPARK} transparent opacity={0.8} />
		</T.Mesh>
	{/each}

	<!-- Middle glow halo -->
	<T.Mesh scale={sparkPulse * 1.2}>
		<T.SphereGeometry args={[0.28, 16, 16]} />
		<T.MeshBasicMaterial color={BLUE_SPARK} transparent opacity={0.25} />
	</T.Mesh>

	<!-- Outer glow sphere - atmosphere -->
	<T.Mesh scale={sparkPulse * 1.8}>
		<T.SphereGeometry args={[0.35, 16, 16]} />
		<T.MeshBasicMaterial color={BLUE_SPARK} transparent opacity={0.08} />
	</T.Mesh>
</T.Group>

<!-- Red Mechanical Band: Machine containment -->
<T.Group rotation.x={Math.PI / 2} rotation.z={ringRotation}>
	<!-- Main containment ring -->
	<T.Mesh>
		<T.TorusGeometry args={[0.6, 0.08, 16, 64]} />
		<T.MeshStandardMaterial
			color={RED_CONTAINMENT}
			metalness={0.8}
			roughness={0.3}
		/>
	</T.Mesh>

	<!-- Secondary precision ring -->
	<T.Mesh rotation.x={Math.PI / 4}>
		<T.TorusGeometry args={[0.55, 0.03, 8, 48]} />
		<T.MeshStandardMaterial
			color={RED_CONTAINMENT}
			metalness={0.9}
			roughness={0.2}
			transparent
			opacity={0.6}
		/>
	</T.Mesh>

	<!-- Mechanical segments on ring -->
	{#each [0, 90, 180, 270] as angle}
		<T.Mesh
			position.x={Math.cos(THREE.MathUtils.degToRad(angle)) * 0.6}
			position.y={Math.sin(THREE.MathUtils.degToRad(angle)) * 0.6}
		>
			<T.BoxGeometry args={[0.1, 0.1, 0.05]} />
			<T.MeshStandardMaterial color={RED_CONTAINMENT} metalness={0.9} roughness={0.1} />
		</T.Mesh>
	{/each}
</T.Group>

<!-- Green/Cyan Emergence: Gestalt structures orbiting outward -->
<T.Group rotation.y={emergenceRotation}>
	<!-- Four emergence structures at cardinal points, growing in complexity -->

	<!-- North: Simple - 1 element -->
	<Float speed={2} floatIntensity={0.1}>
		<T.Group position.y={1.2}>
			<T.Mesh rotation.x={time * 0.5}>
				<T.OctahedronGeometry args={[0.12, 0]} />
				<T.MeshStandardMaterial
					color={GREEN_EMERGENCE}
					emissive={GREEN_EMERGENCE}
					emissiveIntensity={0.3}
					transparent
					opacity={0.9}
				/>
			</T.Mesh>
		</T.Group>
	</Float>

	<!-- East: Growing - 2 elements -->
	<Float speed={1.5} floatIntensity={0.15}>
		<T.Group position.x={1.4}>
			<T.Mesh rotation.y={time * 0.4}>
				<T.OctahedronGeometry args={[0.15, 0]} />
				<T.MeshStandardMaterial
					color={GREEN_EMERGENCE}
					emissive={GREEN_EMERGENCE}
					emissiveIntensity={0.3}
					transparent
					opacity={0.85}
				/>
			</T.Mesh>
			<T.Mesh position.x={0.2} rotation.z={time * 0.6}>
				<T.TetrahedronGeometry args={[0.1, 0]} />
				<T.MeshStandardMaterial
					color={GREEN_EMERGENCE}
					emissive={GREEN_EMERGENCE}
					emissiveIntensity={0.2}
					transparent
					opacity={0.7}
				/>
			</T.Mesh>
		</T.Group>
	</Float>

	<!-- South: Mature - 3 elements (positioned lower to avoid text) -->
	<Float speed={1.2} floatIntensity={0.12}>
		<T.Group position.y={-2.2}>
			<T.Mesh rotation.x={time * 0.3} rotation.y={time * 0.4}>
				<T.IcosahedronGeometry args={[0.18, 0]} />
				<T.MeshStandardMaterial
					color={GREEN_EMERGENCE}
					emissive={GREEN_EMERGENCE}
					emissiveIntensity={0.35}
					transparent
					opacity={0.9}
				/>
			</T.Mesh>
			{#each [-0.2, 0.2] as offset}
				<T.Mesh position.x={offset} position.y={-0.15} rotation.z={time * 0.5}>
					<T.OctahedronGeometry args={[0.08, 0]} />
					<T.MeshStandardMaterial
						color={GREEN_EMERGENCE}
						emissive={GREEN_EMERGENCE}
						emissiveIntensity={0.25}
						transparent
						opacity={0.75}
					/>
				</T.Mesh>
			{/each}
		</T.Group>
	</Float>

	<!-- West: Full mastery - 4 elements, largest -->
	<Float speed={1} floatIntensity={0.18}>
		<T.Group position.x={-1.6}>
			<T.Mesh rotation={[time * 0.2, time * 0.3, time * 0.1]}>
				<T.IcosahedronGeometry args={[0.22, 1]} />
				<T.MeshStandardMaterial
					color={GREEN_EMERGENCE}
					emissive={GREEN_EMERGENCE}
					emissiveIntensity={0.4}
					wireframe
					transparent
					opacity={0.9}
				/>
			</T.Mesh>
			<!-- Inner solid -->
			<T.Mesh rotation={[time * -0.1, time * -0.2, 0]}>
				<T.IcosahedronGeometry args={[0.12, 0]} />
				<T.MeshStandardMaterial
					color={GREEN_EMERGENCE}
					emissive={GREEN_EMERGENCE}
					emissiveIntensity={0.5}
				/>
			</T.Mesh>
			<!-- Orbiting smaller elements -->
			{#each [0, 120, 240] as angle}
				<T.Mesh
					position.x={Math.cos(THREE.MathUtils.degToRad(angle + time * 50)) * 0.3}
					position.y={Math.sin(THREE.MathUtils.degToRad(angle + time * 50)) * 0.3}
				>
					<T.TetrahedronGeometry args={[0.06, 0]} />
					<T.MeshStandardMaterial
						color={GREEN_EMERGENCE}
						emissive={GREEN_EMERGENCE}
						emissiveIntensity={0.3}
						transparent
						opacity={0.8}
					/>
				</T.Mesh>
			{/each}
		</T.Group>
	</Float>
</T.Group>
