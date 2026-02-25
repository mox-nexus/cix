<script lang="ts">
	let copied = $state<string | null>(null);

	const commands = [
		{ label: 'marketplace', cmd: 'claude marketplace add mox-labs/cix', variant: 'spark' as const },
		{ label: 'cli', cmd: 'uvx --from "cix @ git+https://github.com/mox-nexus/cix#subdirectory=tools/cix" cix', variant: 'emergence' as const }
	];

	async function copy(cmd: string) {
		await navigator.clipboard.writeText(cmd);
		copied = cmd;
		setTimeout(() => { if (copied === cmd) copied = null; }, 1500);
	}
</script>

<aside class="quickstart">
	{#each commands as { label, cmd, variant }}
		<div class="method">
			<div class="method-header">
				<span class="label">{label}</span>
				<button
					class="copy-btn"
					class:copied={copied === cmd}
					onclick={() => copy(cmd)}
					title="Copy to clipboard"
					aria-label="Copy {label} command"
				>
					{copied === cmd ? '✓' : '⎘'}
				</button>
			</div>
			<pre class="code-block code-{variant}"><code>{cmd}</code></pre>
		</div>
	{/each}
</aside>

<style>
	.quickstart {
		display: flex;
		flex-direction: column;
		justify-content: center;
		gap: var(--space-2);
		width: 100%;
	}

	.method {
		display: flex;
		flex-direction: column;
		gap: var(--space-0-5);
	}

	.method-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.label {
		font-family: var(--font-mono);
		font-size: var(--type-xs);
		color: var(--dao-muted);
		letter-spacing: var(--tracking-wide);
	}

	.copy-btn {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		color: var(--dao-muted);
		opacity: 0.4;
		background: none;
		border: none;
		cursor: pointer;
		padding: 0;
		transition: opacity var(--duration-fast) var(--easing-linear);
	}

	.copy-btn:hover {
		opacity: 0.8;
	}

	.copy-btn.copied {
		color: var(--emergence-core);
		opacity: 1;
	}

	.code-block {
		font-family: var(--font-mono);
		font-size: var(--type-sm);
		background: var(--dao-surface);
		border: 1px solid var(--dao-border);
		padding: var(--space-1) var(--space-1-5);
		margin: 0;
		overflow-x: auto;
		white-space: pre;
		border-radius: 2px;
	}

	.code-block code {
		background: none;
		padding: 0;
	}

	.code-spark code {
		color: var(--spark-core);
	}

	.code-emergence code {
		color: var(--emergence-core);
	}

	@media (prefers-reduced-motion: reduce) {
		.copy-btn {
			transition: none;
		}
	}
</style>
