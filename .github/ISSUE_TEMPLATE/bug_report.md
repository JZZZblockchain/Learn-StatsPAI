---
name: Bug report
about: Report a crash, incorrect number, documentation error, or behavior that contradicts the docstring/paper
title: "[bug] <short description>"
labels: bug
assignees: ''
---

## Summary

<!-- One sentence: what is wrong. -->

## Environment

- StatsPAI version: <!-- python -c "import statspai as sp; print(sp.__version__)" -->
- Python version: <!-- python --version -->
- OS: <!-- macOS / Linux / Windows + version -->
- Install source: <!-- pip install statspai / pip install -e . / conda / source build -->
- Extras installed (if any): <!-- e.g. [plotting], [fixest], [neural], [performance], [bayes] -->

## Minimal reproducible example

<!--
If at all possible, please use one of the bundled teaching datasets under
`sp.datasets` (mpdta, card_1995, lee_2008_senate, california_prop99, ...)
so we can run the example directly.
-->

```python
import statspai as sp

# your minimal example here
```

## What you expected

<!-- The number / behavior you expected. Reference the docstring, paper,
or reference implementation (Stata / R / other) if applicable. -->

## What actually happened

<!-- Paste the error traceback or the unexpected output. -->

```
<traceback or output here>
```

## Numerical-correctness notes (if applicable)

<!-- For estimator-level numerical issues, fill in:
- Reference implementation tried for comparison (Stata package / R package / source paper)
- Version of that reference (Stata 18, fixest 0.11, did 2.1.2, etc.)
- The number it returns vs. what StatsPAI returns
- A reproducible script if possible
-->

## Anything else

<!-- Logs, screenshots, related issues, suspected cause. -->
