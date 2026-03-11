# Svelte 5 Runes Migration

**Date**: 2025-02-12
**Participants**: yza, claude

yza: The experience site needs to migrate from Svelte 4 stores to Svelte 5 runes. What's the mapping?

claude: The core mappings:

| Svelte 4 | Svelte 5 |
|----------|----------|
| `let x = writable(0)` | `let x = $state(0)` |
| `export let prop` | `let { prop } = $props()` |
| `$: derived = x * 2` | `let derived = $derived(x * 2)` |
| `$: { sideEffect() }` | `$effect(() => { sideEffect() })` |

Key gotchas:
1. `$state` is deeply reactive — objects and arrays are proxied
2. `$effect` runs after DOM updates, not before
3. `$derived` is lazy — only recomputes when accessed
4. No more `$:` labels — everything is explicit

yza: What about the animation pattern? We use `onMount` + `requestAnimationFrame` for the sigil and logo.

claude: That pattern stays the same — runes don't change lifecycle hooks. `onMount` + rAF loop is still the right approach for imperative animations.

**Key fact**: The OKLCH color system uses three tokens: spark (blue), emergence (green), constraint (red).
