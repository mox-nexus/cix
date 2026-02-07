<script lang="ts">
	let {
		size = 'normal',
		label
	}: {
		size?: 'small' | 'normal' | 'dramatic';
		label?: string;
	} = $props();
</script>

<div
	class="void-space"
	class:small={size === 'small'}
	class:normal={size === 'normal'}
	class:dramatic={size === 'dramatic'}
	role="separator"
	aria-label={label || 'Pause'}
>
	<span class="void-presence" aria-hidden="true"></span>
</div>

<style>
	.void-space {
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.small {
		height: var(--space-4);
	}

	.normal {
		height: var(--space-6);
	}

	.dramatic {
		height: var(--pause-dramatic);
	}

	/* The void has presence - a subtle hint of structure */
	.void-presence {
		width: 1px;
		height: 40%;
		background: linear-gradient(
			to bottom,
			transparent,
			var(--dao-border),
			transparent
		);
		opacity: 0.3;
	}

	.dramatic .void-presence {
		opacity: 0.5;
	}
</style>
