# Worked Example — Python data/ML stack starter list

A worked example of a curated mining corpus for the Python data-and-ML domain. Like the Rust exemplar, this is a *demonstration* of what a curated starter list looks like for one domain — adapt the methodology in `references/dataset-selection.md` to build the analogous list for your domain.

Use in Phase 2 (dataset selection — domain mode for "elite Python data/ML libraries"). Pick 3–5 to begin with; expand or trim by goal.

## Contents

- [Numerical core](#numerical-core)
- [Dataframes / I/O](#dataframes--io)
- [ML core](#ml-core)
- [Deep-learning frameworks](#deep-learning-frameworks)
- [Distributed / runtime](#distributed--runtime)
- [Picking from this list](#picking-from-this-list)

## Numerical core

| Repo | Why mine it |
|---|---|
| `numpy/numpy` | The numerical foundation — broadcasting semantics, dtype design, ufunc protocol, multi-decade archaeology |
| `scipy/scipy` | Scientific algorithms; high-quality oscillation history (numerical-stability reverts) and rich `# SAFETY:`-equivalent docstrings about edge cases |

## Dataframes / I/O

| Repo | Why mine it |
|---|---|
| `pandas-dev/pandas` | Dataframe semantics — index design, NA handling oscillations (extension arrays vs object arrays), API surface tradeoffs |
| `pola-rs/polars` | Newer dataframe lib; mining target for *current* idiom (lazy evaluation, expression DSL) — useful comparison vs pandas |
| `apache/arrow` | Columnar memory format; cross-language ABI; rich RFC archaeology |
| `pydantic/pydantic` | Type-driven validation; mining target for *Python type-system as design tool* (closest Python comes to Rust-style invariant encoding in types) |

## ML core

| Repo | Why mine it |
|---|---|
| `scikit-learn/scikit-learn` | The classical-ML library; estimator API design; multi-decade docstring conventions encoding invariants |
| `huggingface/transformers` | Transformer ecosystem; rapid evolution = rich oscillations + deprecation archaeology |

## Deep-learning frameworks

| Repo | Why mine it |
|---|---|
| `pytorch/pytorch` | Most-mined-already DL framework; dynamic-graph semantics; massive RFC and PR archaeology |
| `tensorflow/tensorflow` | Static-graph era artifacts; v1→v2 migration is the largest Python ecosystem migration in history (oscillation gold) |
| `jax-ml/jax` | Functional-programming pattern in Python; transformations (`jit`, `grad`, `vmap`) as the design language |

## Distributed / runtime

| Repo | Why mine it |
|---|---|
| `ray-project/ray` | Distributed compute / actor model in Python; runtime design tradeoffs |
| `dask/dask` | Lazy distributed dataframes/arrays; comparison target with ray + polars |

---

## Picking from this list

| Goal | Start with |
|---|---|
| Numerical-API design tradeoffs | numpy + scipy + jax |
| Dataframe semantics | pandas + polars + arrow |
| ML estimator API design | scikit-learn + huggingface/transformers |
| Migration archaeology (v1→v2) | tensorflow + huggingface/transformers |
| Type-system-as-design (Python's version) | pydantic + jax |
| Functional-programming idioms in Python | jax + ray |

## Notes for Python mining

- **Scar density**: Python's `# NOTE:` / `# WARNING:` / `# TODO:` markers are less convention-driven than Rust's `// SAFETY:`. Lean on docstrings (`""" Notes / Warnings / Raises """`) and `# noqa: <code>` annotations as additional scar surfaces.
- **Signatures**: Python's gradual typing reduces signature density vs Rust. Compensate by mining `Protocol` classes, `TypeVar` definitions, `@overload` declarations, and `dataclass` / `pydantic.BaseModel` definitions — these are the closest Python analogs to Rust's typed-shape signal.
- **Decorator chains** are the most Python-specific signature surface. `@functools.cached_property`, `@contextmanager`, `@classmethod`-`@property` interactions, custom decorators stacked together — these encode design choices that have no Rust analog.
- **Tests-as-spec**: Python's `pytest.raises(...)` patterns and parametrize names often encode invariants more clearly than the source code. Lean harder on `tests/` mining than for typed languages.
- **Cython / C-extension boundaries**: numpy / pandas / pytorch have parts written in C / C++ / Cython. Treat the boundary as its own scar-rich surface — the FFI layer is where invariants get explicit.
