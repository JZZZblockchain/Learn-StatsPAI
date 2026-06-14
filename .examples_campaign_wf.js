export const meta = {
  name: 'statspai-examples-campaign',
  description: 'Add verified Examples blocks to functions missing them, partitioned by source file (zero write races)',
  phases: [
    { title: 'Write', detail: 'one agent per file-bundle, every example executed' },
    { title: 'Verify', detail: 'independent re-run of every example + docstring-only diff audit' },
  ],
}

const REPO = '/Users/brycewang/Documents/GitHub/StatsPAI'
const CAMPAIGN = args && args.campaign ? args.campaign : 'campaign1'
const BUNDLES_PATH = (args && args.bundlesPath) ? args.bundlesPath : '/tmp/example_bundles.json'
const REMEDIATE = !!(args && args.remediate)

const COMMON = `
You are improving docstrings in StatsPAI at ${REPO} (import statspai as sp; NumPy docstring style; mkdocstrings renders docstrings into the public API site; JOSS review checklist requires example usage).

HARD RULES — violating any of these fails the task:
0. GIT IS OFF-LIMITS: never run git add / commit / push / stash / checkout. Read-only git (diff/status/show) is fine. The orchestrator commits.
1. ONLY docstring text may change. No signature/logic/import/formatting change outside the docstring string. Verify with: git diff -- <file> shows only inserted lines inside a triple-quoted docstring.
2. EVERY Examples block MUST be executed before you write it in: extract the exact example code to /tmp/ex_<func>.py, run 'MPLBACKEND=Agg python3 /tmp/ex_<func>.py', confirm exit 0. Keep each under ~10 seconds (small n; reduce bootstrap/draw kwargs via the function's real params; fixed seeds).
3. Find each PUBLIC def with: python3 -c "import statspai as sp, inspect; print(inspect.getsourcefile(inspect.unwrap(sp.<name>)))" and inspect.signature(sp.<name>). Edit the def site shown in your bundle. Some names are aliases pointing at the same object in the same file — if adding Examples to one name already covers another (same object), skip the duplicate and note it.
4. STYLE: mirror an existing Examples block in the SAME module/file (grep 'Examples' in nearby files). Start every block with '>>> import statspai as sp'. Use bundled datasets (check src/statspai/datasets/ — e.g. sp.cps_wage(), sp.mincer_wage_panel(), sp.california_prop99(), sp.nhefs() if present) or tiny inline numpy default_rng(seed) simulated data. Do NOT print raw floats that drift across BLAS; wrap truthy checks in bool(...) (numpy 2.x prints np.True_); show only stable values in trailing comments and only if you verified them verbatim. Plot functions: run under MPLBACKEND=Agg, capture (fig, ax) / returned object, mark savefig lines '# doctest: +SKIP', never call plt.show().
5. CITATIONS: add a References line ONLY with a bib key you grep-confirmed already exists in ${REPO}/paper.bib. NEVER invent a citation. If unsure, omit References entirely.
6. SKIP HONESTLY (do not fabricate): if a function needs heavy optional deps you cannot run fast (torch/jax/pymc/transformers), genuinely cannot be called directly (abstract/base/dispatch-only that errors), or cannot be exercised in <~15s, SKIP it and record the reason. A skipped function with a clear reason is correct; an unverified or non-running example is a FAILURE.
7. If a function ALREADY has an Examples section on inspection, skip it (note 'already had Examples').
`

const WRITE_SCHEMA = {
  type: 'object',
  properties: {
    done: { type: 'array', items: { type: 'object', properties: {
      func: { type: 'string' }, file: { type: 'string' }, ran_ok: { type: 'boolean' },
    }, required: ['func', 'file', 'ran_ok'] } },
    skipped: { type: 'array', items: { type: 'object', properties: {
      func: { type: 'string' }, reason: { type: 'string' },
    }, required: ['func', 'reason'] } },
    files_touched: { type: 'array', items: { type: 'string' } },
    notes: { type: 'string' },
  },
  required: ['done', 'skipped', 'files_touched', 'notes'],
}

const VERIFY_SCHEMA = {
  type: 'object',
  properties: {
    verdict: { type: 'string', enum: ['approve', 'needs_rework'] },
    examples_rerun: { type: 'integer' },
    examples_failed: { type: 'integer' },
    non_docstring_changes_found: { type: 'boolean' },
    problems: { type: 'array', items: { type: 'string' } },
  },
  required: ['verdict', 'examples_rerun', 'examples_failed', 'non_docstring_changes_found', 'problems'],
}

// Read the bundle list to learn how many bundles this campaign has.
// The script itself cannot read files, so an agent reports the count first.
const countAgent = await agent(
  `Read ${BUNDLES_PATH} (python3 -c "import json;d=json.load(open('${BUNDLES_PATH}'));print(len(d['${CAMPAIGN}']))"). Return ONLY that integer.`,
  { label: 'bundle-count', phase: 'Write', schema: { type: 'object', properties: { n: { type: 'integer' } }, required: ['n'] } }
)
const N = countAgent ? countAgent.n : 0
log(`${CAMPAIGN}: ${N} bundles to process`)

const indices = Array.from({ length: N }, (_, i) => i)

const results = await pipeline(
  indices,
  i => agent(`${COMMON}
${REMEDIATE ? `
REMEDIATION MODE — IMPORTANT: many functions in your bundle CURRENTLY HAVE A NON-RUNNING Examples block (it references an undefined variable like df / bx / m1 / a bare unqualified function name, or was left half-written). These are FAILURES that must be repaired. For every such function you MUST REPLACE the broken Examples block with one that ACTUALLY EXECUTES: add an explicit data-setup line (a bundled dataset such as sp.cps_wage() / sp.mincer_wage_panel() / sp.nhefs() if it exists, or a tiny inline numpy default_rng(seed) DataFrame with the exact columns the call needs), call sp.<func>(...) with the real signature, and RUN the whole block (exit 0) before saving. Do not leave any '>>>' line that references an undefined name. After editing, re-extract the block and run it to PROVE it works.` : ''}
TASK: process bundle index ${i} of campaign '${CAMPAIGN}'. First load YOUR bundle:
  python3 -c "import json;d=json.load(open('${BUNDLES_PATH}'));b=d['${CAMPAIGN}'][${i}];import sys;print(json.dumps(b))"
It is a list of {file, funcs:[...]} — the functions in those files that lack an Examples section. Add a verified Examples block to each function's docstring per the rules. Work file-by-file. No other bundle touches your files, so there are no write conflicts. Report per-function ran_ok, the files you touched, and any honest skips with reasons.`,
    { label: `write:${CAMPAIGN}#${i}`, phase: 'Write', schema: WRITE_SCHEMA }),
  (res, i) => {
    if (!res) return null
    return agent(`${COMMON}

You are an independent VERIFIER for bundle ${i} of campaign '${CAMPAIGN}'. The writer reported: done=${JSON.stringify(res.done)} skipped=${JSON.stringify(res.skipped)} files=${JSON.stringify(res.files_touched)}.
1. For EACH file in files_touched: git diff -- <file> and confirm every changed hunk is inside a docstring (inserted Examples/References lines only). Any code/signature/import change => non_docstring_changes_found=true, needs_rework.
2. For EACH 'done' function: extract its current docstring example (python3 -c "import statspai as sp,inspect;print(inspect.getdoc(sp.<f>))"), write the example lines to /tmp and run 'MPLBACKEND=Agg python3 ...'. Count examples_rerun and examples_failed. ANY failure => needs_rework.
3. Spot-check that skips were legitimate (a skipped function that actually runs fine in <10s and could have had an example is a minor problem, not a blocker — note it).
4. Confirm 'import statspai' still works. Verify no invented citations: every new [@key] grep-exists in paper.bib.
Report verdict. Do not invent problems; if the bundle is clean, approve.`,
      { label: `verify:${CAMPAIGN}#${i}`, phase: 'Verify', schema: VERIFY_SCHEMA }).then(v => ({ i, write: res, verify: v }))
  },
  (pair, i) => {
    if (!pair) return null
    if (pair.verify.verdict === 'approve') return pair
    return agent(`${COMMON}

TASK: REWORK bundle ${i} of '${CAMPAIGN}'. Verifier rejected with: ${JSON.stringify(pair.verify.problems)} (non_docstring_changes=${pair.verify.non_docstring_changes_found}, failed=${pair.verify.examples_failed}). Independently reproduce each problem, fix it (revert any non-docstring change manually; repair or remove any non-running example — a removed bad example is better than a broken one), re-run every example. Report final state.`,
      { label: `rework:${CAMPAIGN}#${i}`, phase: 'Write', schema: WRITE_SCHEMA }).then(r => ({ ...pair, rework: r }))
  }
)

const out = results.filter(Boolean)
const totalDone = out.reduce((n, r) => n + (r.write ? r.write.done.filter(d => d.ran_ok).length : 0), 0)
const totalSkip = out.reduce((n, r) => n + (r.write ? r.write.skipped.length : 0), 0)
const reworks = out.filter(r => r.rework).length
log(`${CAMPAIGN} done: ${totalDone} examples added, ${totalSkip} skipped, ${reworks} bundles reworked`)
return { campaign: CAMPAIGN, bundles: out.length, added: totalDone, skipped: totalSkip, reworks,
  detail: out.map(r => ({ i: r.i, verdict: r.verify.verdict, added: r.write.done.filter(d => d.ran_ok).length, skipped: r.write.skipped.length })) }
