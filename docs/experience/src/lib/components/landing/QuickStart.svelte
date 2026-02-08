<script lang="ts">
	let copied = $state<string | null>(null);

	const commands = [
		{ label: 'cli', cmd: 'uv tool install cix', variant: 'emergence' as const },
		{ label: 'marketplace', cmd: 'claude plugin marketplace add mox-nexus/cix', variant: 'spark' as const }
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
			<span class="label">{label}</span>
			<button
				class="cmd cmd-{variant}"
				class:copied={copied === cmd}
				onclick={() => copy(cmd)}
				title="Copy to clipboard"
			>
				<code>{cmd}</code>
				<span class="copy-indicator" aria-hidden="true">
					{copied === cmd ? '✓' : '⎘'}
				</span>
			</button>
		</div>
	{/each}
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
		cursor: pointer;
		display: flex;
		align-items: center;
		gap: var(--space-1);
		transition: border-color var(--duration-fast) var(--easing-linear);
	}

	.cmd:hover {
		border-color: var(--dao-text-secondary);
	}

	.cmd.copied {
		border-color: var(--emergence-core);
	}

	.cmd-emergence code {
		color: var(--emergence-core);
	}

	.cmd-spark code {
		color: var(--spark-core);
	}

	.cmd code {
		white-space: nowrap;
	}

	.copy-indicator {
		font-size: var(--type-sm);
		color: var(--dao-muted);
		opacity: 0.4;
		transition: opacity var(--duration-fast) var(--easing-linear);
	}

	.cmd:hover .copy-indicator {
		opacity: 0.8;
	}

	.cmd.copied .copy-indicator {
		color: var(--emergence-core);
		opacity: 1;
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

	@media (prefers-reduced-motion: reduce) {
		.cmd,
		.copy-indicator {
			transition: none;
		}
	}
</style>
