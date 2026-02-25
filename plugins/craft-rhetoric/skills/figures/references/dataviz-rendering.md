# Dataviz Rendering Reference

When static diagrams (Mermaid, D2, C4) aren't enough — the visual needs motion, interactivity, or rendered data.

## THE Decision

**Default to Mermaid** for documentation diagrams. Upgrade to rendered dataviz when:
- The visual needs **animation** (particles, morphing, scroll-driven reveals)
- The data is **quantitative** and needs axes, scales, or interpolation
- The visual must be **interactive** (hover, zoom, filter, brush)
- The explanation requires **cinematic impact** (ethos pages, landing visuals)
- Static text-in-markdown can't carry the information structure

## Library Routing

| Need | Library | Why |
|------|---------|-----|
| Custom SVG/Canvas, full control | **D3** | Imperative, bindable, production standard |
| Svelte-native charts | **LayerChart** | Svelte 5 runes, composable, D3-powered |
| Declarative grammar-of-graphics | **Observable Plot** | Concise spec, good defaults |
| Cinematic SVG animation | **Hand-rolled SVG + rAF** | Full control, no dependencies |
| Scroll-driven animation | **CSS `animation-timeline`** or **GSAP ScrollTrigger** | Native or battle-tested |
| WebGL / 3D | **Three.js** or **threlte** (Svelte) | When 2D isn't enough |

## D3.js

The standard for custom data visualization. Bindable to DOM. Pairs with SVG or Canvas.

**Use when**: Custom layouts, force simulations, geographic maps, anything off the shelf doesn't cover.

```typescript
import * as d3 from 'd3';

// Select + bind data
const circles = d3.select('svg')
  .selectAll('circle')
  .data(dataset)
  .join('circle')
  .attr('cx', d => xScale(d.x))
  .attr('cy', d => yScale(d.y))
  .attr('r', d => rScale(d.value));

// Transitions
circles.transition()
  .duration(800)
  .attr('r', d => rScale(d.newValue));
```

**Scales**: `d3.scaleLinear()`, `d3.scaleLog()`, `d3.scaleBand()`, `d3.scaleOrdinal()`
**Shapes**: `d3.line()`, `d3.area()`, `d3.arc()`, `d3.curveCatmullRom`
**Layouts**: `d3.forceSimulation()`, `d3.treemap()`, `d3.pack()`, `d3.hierarchy()`
**Selections**: `d3.select()`, `.join()` (enter/update/exit in one call)

**With Svelte**: Use D3 for math (scales, shapes, layouts). Use Svelte for DOM (reactivity, transitions). Don't let D3 own the DOM — compute data with D3, render with `{#each}`.

```svelte
<script>
  import { scaleLinear } from 'd3-scale';
  import { line, curveCatmullRom } from 'd3-shape';

  let { data } = $props();
  let x = $derived(scaleLinear().domain([0, data.length]).range([0, width]));
  let y = $derived(scaleLinear().domain([0, d3.max(data)]).range([height, 0]));
  let path = $derived(line().x((_, i) => x(i)).y(d => y(d)).curve(curveCatmullRom)(data));
</script>

<svg>
  <path d={path} fill="none" stroke="currentColor" />
</svg>
```

## LayerChart

Svelte-native charting. Built on D3 scales. Uses Svelte 5 runes.

**Use when**: Standard chart types in a SvelteKit project. Composable component API.

```svelte
<script>
  import { Chart, Svg, Axis, Spline, Highlight, Tooltip } from 'layerchart';
  import { scaleTime, scaleLinear } from 'd3-scale';
</script>

<Chart data={timeSeries} x="date" y="value"
  xScale={scaleTime()} yScale={scaleLinear()} padding={{ left: 40, bottom: 24 }}>
  <Svg>
    <Axis placement="left" />
    <Axis placement="bottom" />
    <Spline class="stroke-blue-500" />
    <Highlight points lines />
  </Svg>
  <Tooltip />
</Chart>
```

**Strengths**: Composable (mix Chart + Svg + Canvas layers), theme-aware, SSR-safe
**Limitations**: Opinionated component API, less flexible than raw D3 for custom layouts

## SVG Animation Patterns

For cinematic, scroll-triggered, or continuous animation. No library needed — just SVG + rAF.

### rAF + Delta-Time Loop

The foundational pattern for frame-rate-independent animation:

```typescript
onMount(() => {
  let animationId: number;
  let lastTime = performance.now();

  const animate = (currentTime: number) => {
    const delta = currentTime - lastTime; // ms since last frame
    lastTime = currentTime;

    // Use delta for speed — never raw frame count
    progress += speed * delta; // speed in units/ms

    animationId = requestAnimationFrame(animate);
  };

  animationId = requestAnimationFrame(animate);
  return () => cancelAnimationFrame(animationId);
});
```

**Delta-time matters**: `progress += 1` runs 2x faster at 120fps vs 60fps. Always multiply by delta.

### Staged Reveal

Sequence elements by elapsed time, not frame count:

```typescript
const elapsed = currentTime - startedAt;

if (elapsed < 1500) phase = 1;      // Path draws
else if (elapsed < 3000) phase = 2;  // Labels fade
else if (elapsed < 5000) phase = 3;  // Particles flow
else phase = 4;                       // Final state
```

Combine with Svelte conditionals:
```svelte
{#if phase >= 2}
  <g class="label-fade">...</g>
{/if}
```

### SVG Path Animation (Stroke-Dashoffset)

Draw a path progressively:

```svelte
<path
  d={pathData}
  stroke-dasharray={totalLength}
  stroke-dashoffset={totalLength * (1 - progress)}
/>
```

Measure path length: `pathElement.getTotalLength()` or estimate from geometry.

### SVG Filters for Glow

Layered blur for cinematic glow effects:

```svg
<filter id="glow" x="-200%" y="-200%" width="500%" height="500%">
  <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur1"/>
  <feGaussianBlur in="SourceGraphic" stdDeviation="8" result="blur2"/>
  <feMerge>
    <feMergeNode in="blur2"/>   <!-- Wide glow -->
    <feMergeNode in="blur1"/>   <!-- Tight glow -->
    <feMergeNode in="SourceGraphic"/>  <!-- Sharp core -->
  </feMerge>
</filter>
```

**Filter region**: `x="-200%" y="-200%" width="500%" height="500%"` — SVG clips filter output to element bbox by default. Expand to prevent clipping.

### Easing Functions

```typescript
// Smoothstep — slow start and end
const smoothstep = (t: number) => t * t * (3 - 2 * t);

// Ease-out cubic
const easeOut = (t: number) => 1 - Math.pow(1 - t, 3);

// Pulse / breathing
const pulse = (time: number, freq: number = 0.003) =>
  0.6 + 0.4 * Math.sin(time * freq);
```

### Interpolation Between States

Morph between parameter sets:

```typescript
function lerp(a: number, b: number, t: number): number {
  return a + (b - a) * t;
}

// Interpolate full config objects
function lerpConfig(a: Config, b: Config, t: number): Config {
  return {
    width: lerp(a.width, b.width, t),
    height: lerp(a.height, b.height, t),
    opacity: lerp(a.opacity, b.opacity, t)
  };
}
```

### Gaussian Curve Generation

For distribution visualizations:

```typescript
function gaussianPath(cx: number, width: number, height: number, baseY: number): string {
  const steps = 100;
  const points: string[] = [];
  for (let i = 0; i <= steps; i++) {
    const x = cx - width/2 + (width * i / steps);
    const normalized = (x - cx) / (width / 4.5);
    const y = height * Math.exp(-0.5 * normalized * normalized);
    points.push(`${x.toFixed(1)},${(baseY - y).toFixed(1)}`);
  }
  return `M ${points[0]} ` + points.slice(1).map(p => `L ${p}`).join(' ');
}
```

## Scroll-Driven Animation

### CSS `animation-timeline` (Native)

Zero-JS scroll-linked animation. Chrome 115+, Firefox 110+, Safari limited.

```css
.element {
  animation: reveal linear both;
  animation-timeline: scroll();
  animation-range: entry 0% cover 40%;
}

@keyframes reveal {
  from { opacity: 0; transform: translateY(24px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### IntersectionObserver (Universal)

Trigger animation when elements enter viewport:

```typescript
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        visibleSet.add(entry.target.dataset.id);
      }
    });
  },
  { rootMargin: '-10% 0% -20% 0%' }
);
```

**rootMargin**: Negative values delay trigger until element is well into viewport. Good for "scroll and reveal" patterns.

### GSAP ScrollTrigger

Production scroll animation. Pinning, scrubbing, snapping.

```typescript
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

gsap.to('.element', {
  scrollTrigger: {
    trigger: '.section',
    start: 'top center',
    end: 'bottom center',
    scrub: true, // Ties animation to scroll position
    pin: true    // Pins element during scroll range
  },
  opacity: 1,
  y: 0
});
```

**Use when**: Complex scroll choreography, pinned sections, parallax. GSAP is battle-tested but adds ~30KB.

## Accessibility

Every animated visual MUST handle reduced motion:

```typescript
// Detect in JS
const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
if (mq.matches) {
  // Jump to final state, skip animation
  phase = FINAL;
  return;
}
```

```css
/* CSS fallback */
@media (prefers-reduced-motion: reduce) {
  .animated { transition: none; animation: none; }
}
```

**Static fallback**: When animation is skipped, the final state must still communicate the information. If the animation IS the explanation (e.g., particles dimming = "thinner each cycle"), add text annotations visible in reduced-motion mode.

## Performance

| Concern | Solution |
|---------|----------|
| Too many SVG filters | Limit `feGaussianBlur` count. Each filter pass is a full-surface operation |
| Too many animated elements | Consider Canvas over SVG for 100+ animated items |
| Layout thrashing | Read layout properties once, write once. Batch DOM reads/writes |
| rAF not firing | `cancelAnimationFrame` in cleanup. Gate on `visible` flag |
| Mobile jank | Reduce particle counts, simplify filters, test on real devices |

**GPU promotion**: `transform` and `opacity` are composited on GPU. `width`, `height`, `top` cause layout. Animate only compositable properties when possible.

## When to Use What

| Visual goal | Approach | Libraries |
|-------------|----------|-----------|
| Documentation diagram | Static text-in-markdown | Mermaid, D2, C4 |
| Standard chart (bar, line, area) | Svelte component | LayerChart |
| Custom chart with unusual layout | D3 math + Svelte render | d3-scale, d3-shape |
| Cinematic reveal, flowing particles | Hand-rolled SVG + rAF | None (vanilla) |
| Scroll-triggered appearance | IntersectionObserver | None (vanilla) |
| Scroll-scrubbed animation | GSAP or CSS scroll-timeline | gsap/ScrollTrigger |
| Data dashboard | Full library | LayerChart or Observable Plot |
| Geographic / spatial | D3 geo projections | d3-geo |
| 3D scene | WebGL | Three.js / threlte |

---

**Sources**: D3 official docs (d3js.org), LayerChart docs (layerchart.com), MDN Web Animations API, GSAP docs (gsap.com), web.dev scroll-driven animations guide
