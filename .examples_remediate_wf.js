export const meta = {
  name: 'statspai-examples-remediate',
  description: 'Repair non-running Examples and fill remaining gaps; partitioned by file (zero write races)',
  phases: [
    { title: 'Write', detail: 'one agent per small file-bundle; every example must execute' },
    { title: 'Verify', detail: 'extract >>> lines, drop +SKIP, exec — must not raise' },
  ],
}

const REPO = '/Users/brycewang/Documents/GitHub/StatsPAI'
const PATH = '/tmp/example_remediate.json'

const COMMON = `
You are improving docstrings in StatsPAI at ${REPO} (import statspai as sp; NumPy docstring style; mkdocstrings publishes docstrings; JOSS requires runnable example usage).

HARD RULES (violating any fails the task):
0. GIT IS OFF-LIMITS: never git add/commit/push/stash/checkout. Read-only git is fine. The orchestrator commits.
1. ONLY docstring text changes. No signature/logic/import/format change outside the docstring string.
2. EXECUTION IS THE GATE. For each function, the Examples block you leave behind MUST run start-to-finish with exit 0 when you extract its '>>>'/'...' source lines (dropping any line marked '# doctest: +SKIP') and run them together. Prove it: write the lines to /tmp/ex.py and run 'MPLBACKEND=Agg python3 /tmp/ex.py'. Under ~12s each (small n; reduce bootstrap/draw kwargs; fixed seeds).
3. MANY targets currently have a BROKEN, NON-RUNNING example — it references an undefined name (df, bx, m1, sx/sy, ...), uses a bare unqualified call (e.g. 'mediate(' instead of 'sp.mediate('), or was left half-written. You MUST REPLACE such a block with a self-contained runnable one: add the data-setup line(s) it needs (a bundled dataset — check src/statspai/datasets/, e.g. sp.cps_wage(), sp.mincer_wage_panel(), sp.california_prop99(), sp.nhefs(); or a tiny inline numpy default_rng(seed) DataFrame with exactly the columns the call uses), then call sp.<func>(...) with the REAL signature (inspect.signature first). No '>>>' line may reference an undefined name.
4. Resolve each def site: python3 -c "import statspai as sp, inspect; print(inspect.getsourcefile(inspect.unwrap(sp.<name>)))". Aliases sharing one object in one file: fix once, note the duplicate.
5. STYLE: '>>> import statspai as sp' first; mirror a nearby existing Examples block. Don't print BLAS-drifting floats; wrap truthy checks in bool(...) (numpy 2.x prints np.True_); only show output values you verified verbatim. Plots: MPLBACKEND=Agg, capture (fig, ax), mark savefig '# doctest: +SKIP', never plt.show().
6. CITATIONS: References line only with a bib key you grep-confirmed in ${REPO}/paper.bib. Never invent one.
7. SKIP HONESTLY only if a function truly needs heavy deps you cannot run fast (torch/jax/pymc/transformers) or genuinely cannot be called directly. A skip with a clear reason is fine; a NON-RUNNING example is a FAILURE. Prefer making it run over skipping.
`

const WRITE_SCHEMA = {
  type: 'object',
  properties: {
    fixed: { type: 'array', items: { type: 'string' } },
    skipped: { type: 'array', items: { type: 'object', properties: { func: { type: 'string' }, reason: { type: 'string' } }, required: ['func', 'reason'] } },
    files_touched: { type: 'array', items: { type: 'string' } },
    notes: { type: 'string' },
  },
  required: ['fixed', 'skipped', 'files_touched', 'notes'],
}
const VERIFY_SCHEMA = {
  type: 'object',
  properties: {
    verdict: { type: 'string', enum: ['approve', 'needs_rework'] },
    examples_rerun: { type: 'integer' },
    examples_failed: { type: 'integer' },
    failing_funcs: { type: 'array', items: { type: 'string' } },
    non_docstring_changes_found: { type: 'boolean' },
  },
  required: ['verdict', 'examples_rerun', 'examples_failed', 'failing_funcs', 'non_docstring_changes_found'],
}

const countAgent = await agent(
  `python3 -c "import json;print(len(json.load(open('${PATH}'))['remediate']))" — return ONLY that integer.`,
  { label: 'count', phase: 'Write', schema: { type: 'object', properties: { n: { type: 'integer' } }, required: ['n'] } }
)
const N = countAgent ? countAgent.n : 0
log(`remediate: ${N} bundles`)

const results = await pipeline(
  Array.from({ length: N }, (_, i) => i),
  i => agent(`${COMMON}

TASK: bundle index ${i}. Load it:
  python3 -c "import json;b=json.load(open('${PATH}'))['remediate'][${i}];print(__import__('json').dumps(b))"
It is a list of {file, funcs:[...]}. For EVERY function: ensure its Examples block RUNS (replace broken ones; add missing ones). No other bundle touches your files. Report fixed (func names whose example now runs), honest skips, files touched.`,
    { label: `fix#${i}`, phase: 'Write', schema: WRITE_SCHEMA }),
  (res, i) => {
    if (!res) return null
    return agent(`${COMMON}

INDEPENDENT VERIFIER, bundle ${i}. Writer reported fixed=${JSON.stringify(res.fixed)} skipped=${JSON.stringify((res.skipped || []).map(s => s.func))} files=${JSON.stringify(res.files_touched)}.
For EACH file in files_touched: 'git diff -- <file>' — every changed hunk must be inside a docstring; any code change => non_docstring_changes_found=true + needs_rework.
For EACH 'fixed' func: python3 -c "import statspai as sp,inspect;print(inspect.getdoc(sp.<f>))", take the Examples block, keep only '>>>'/'...' source lines, DROP lines containing '# doctest: +SKIP', write to /tmp and run 'MPLBACKEND=Agg python3'. Count examples_rerun / examples_failed; list failing_funcs. ANY raise => needs_rework. Confirm 'import statspai' works and no invented [@cite] (grep paper.bib). Approve only if examples_failed==0 and no code changes.`,
      { label: `verify#${i}`, phase: 'Verify', schema: VERIFY_SCHEMA }).then(v => ({ i, write: res, verify: v }))
  },
  (pair, i) => {
    if (!pair) return null
    if (pair.verify.verdict === 'approve') return pair
    return agent(`${COMMON}

REWORK bundle ${i}. Verifier found failing examples: ${JSON.stringify(pair.verify.failing_funcs)} (non_docstring_changes=${pair.verify.non_docstring_changes_found}). For each failing func, make its Examples block actually run (fix the setup / signature, or as a last resort remove the broken example entirely — a missing example beats a broken one). Revert any non-docstring change. Re-run every example to prove exit 0.`,
      { label: `rework#${i}`, phase: 'Write', schema: WRITE_SCHEMA }).then(r => ({ ...pair, rework: r }))
  }
)

const out = results.filter(Boolean)
const fixed = out.reduce((n, r) => n + (r.write ? r.write.fixed.length : 0), 0)
const reworked = out.filter(r => r.rework).length
const stillBad = out.filter(r => r.verify && r.verify.verdict === 'needs_rework').map(r => r.i)
log(`remediate done: ${fixed} examples now runnable, ${reworked} bundles reworked, residual-flagged bundles: ${JSON.stringify(stillBad)}`)
return { bundles: out.length, fixed, reworked, stillBad }
