<script lang="ts">
	interface Props {
		uvCmd?: string;
		pluginCmd?: string;
	}

	let {
		uvCmd = 'uv tool install cix',
		pluginCmd = '/plugin add mox-labs/cix'
	}: Props = $props();
</script>

<aside class="quickstart">
	<div class="method">
		<span class="label">cli</span>
		<pre class="cmd"><code>{uvCmd}</code></pre>
	</div>
	<div class="method">
		<span class="label">claude code</span>
		<pre class="cmd plugin"><code>{pluginCmd}</code></pre>
	</div>
</aside>

<style>
	.quickstart {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: var(--space-1);
	}

	.method {
		display: flex;
		align-items: center;
		gap: var(--space-1);
	}

	.label {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		letter-spacing: var(--tracking-wide);
		white-space: nowrap;
		min-width: 9ch;
		text-align: right;
	}

	.cmd {
		font-family: var(--font-mono);
		font-size: var(--type-base);
		background: var(--dao-surface);
		border: 1px solid var(--dao-border);
		padding: var(--space-0-5) var(--space-1-5);
		margin: 0;
		color: var(--emergence-core);
	}

	.cmd.plugin {
		color: var(--spark-core);
	}

	.cmd code {
		white-space: nowrap;
	}

	@media (max-width: 768px) {
		.method {
			flex-direction: column;
			gap: var(--space-0-5);
		}

		.label {
			text-align: center;
			min-width: auto;
		}
	}
</style>
