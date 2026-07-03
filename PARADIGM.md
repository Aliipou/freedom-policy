# The Freedom paradigm — operational core, honest status

This is the theory's **decision machinery** implemented on the value-neutral
`decision-os-min` kernel — and the one place the session moved a real needle: the
conflict-resolution "hardest gap" now has a **derived, tested solution**, not a
defer-to-human punt.

## What the paradigm *is* (as executable structure)

```
Ownership Resolution  →  Consent Verification  →  Freedom Verifier
   (ownership.py)          (consent.py)            (freedom.py)
      → Conflict Resolution (conflict.py)  → Kernel (neutral) → PEP → Audit
```

## Stage status — updated (vs the FDK branch's own assessment)

| Stage | Was (FDK `paradigm/stages-2-9`) | Now (here) |
|---|---|---|
| **2 · Rights Ontology** | "thin — needs expansion" | ✅ ownership axioms enforced (`ownership.py`) + AuthGate `registry`/`inalienable` |
| **Consent Logic** | present | ✅ `valid_consent` (`consent.py`) |
| **Freedom Verifier** | present | ✅ forbidden/permissible (`freedom.py`) |
| **4 · Conflict resolution** | **"OPEN — the hardest gap; defer-to-human"** | ⬆️ **derived solution (`conflict.py`, 4 tests)** — resolves the clear cases from the axioms, defers only genuine ties |
| **9 · Comparative (beats RLHF/CAI/OPA?)** | "unproven — the actual scientific claim" | ⏳ still unproven (one strawman experiment only) |

## The Stage-4 result — what was derived

The theory says *resolve by ownership clarification, never by sacrificing a right.*
The prior implementations stopped at "scope-specificity + read>write + defer." The
axioms actually give more:

1. **Inalienable primacy** — a person's body / mind / consent / **data about them**
   are inalienably theirs; anyone else's claim on that resource is *derived*.
2. **Consent scope** — a derived claim is valid only within the consent the owner
   granted; outside it, the derived claim is void.
3. **Reversibility preference** — when two inalienable claims collide, prefer the
   reversible action; never commit an irreversible violation while resolving.
4. **No right sacrificed / human only for genuine ties.**

This *resolves* "can Alice sell Bob's data?" → **No** (Bob's inalienable data
ownership, out of consent scope) — a case the "hardest gap" deferred on.

## What "it works" honestly means — and does NOT

- ✅ **Works as a formal resolution ladder** on well-specified inputs — it derives
  the right winner from the axioms and defers only true ties. Tested.
- ⚠️ **Depends on DECLARED facts** — "who inalienably owns this datum" (provenance)
  and "is this within consent scope" are *inputs*, not detected. That detection is
  the attested→detected gap and remains unsolved.
- ⚠️ **Self-authored + self-tested.** A first-party result; not independent validation.
- ❌ **The scientific claim (Stage 9) is still unproven** — no measured comparison vs
  OPA/Cedar/RLHF/Constitutional AI on a shared workload.

## Honest bottom line

The paradigm's **operational core now works end-to-end** — ownership, consent,
verifier, and (newly) principled conflict resolution — on a neutral, auditable
kernel. That is a real result: the theory *is* consistent enough to derive its own
hardest rule. What remains is **detection** (turning declared facts into verified
ones) and **validation** (Stage 9 — does it beat the alternatives, measured by
someone who isn't the author). The philosophy stays a closed negative result; the
*engineering* of its decision machinery is, now, largely real and tested.
