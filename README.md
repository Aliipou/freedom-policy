# freedom-policy — the Theory of Freedom, implemented on a neutral kernel

The **operational core** of the Theory of Freedom (نظریه آزادی), expressed entirely
as policy on the value-neutral [`decision-os-min`](https://github.com/Aliipou/decision-os-min)
kernel. **The kernel is not modified** — the whole theory lives here.

```python
from dos_freedom import OwnershipRegistry, ConsentLedger, FreedomGate

reg = OwnershipRegistry()
reg.register_person("alice"); reg.register_machine("bot", owner="alice")
reg.own_resource("alice", "customer_db"); reg.delegate("alice", "bot", "customer_db")

gate = FreedomGate(reg, ConsentLedger(), audit_path="audit.jsonl")
gate.act("bot", {"resource": "customer_db"}, TOOLS)   # permitted -> runs, audited
gate.act("bot", {"resource": "alice"}, TOOLS)          # machine-sovereignty -> forbidden
```

## What's implemented (runnable, tested — 8 tests)

| Theory component | Status |
|---|---|
| **Rights Ontology + Ownership Registry** (God→Human→Machine, delegation, scope⊆owner) | ✅ enforced as invariants |
| **Consent Logic** (`valid_consent`: informed/voluntary/specific/revocable/competent/¬coerced/¬deceived) | ✅ |
| **Freedom Verifier** (`forbidden` :- property-rights / coercion / deception / machine-sovereignty / bypass) | ✅ |
| **Runtime Enforcement** (authorization + PEP + tamper-evident audit) | ✅ (the neutral kernel) |
| **Divine Justice / Guidance / Mahdavi** | ⚠️ value functions, advisory — *not* proven optimizers |

## Honest boundaries (stated, not hidden)

- **This implements the theory's *executable structure*. It does NOT claim the
  theory's philosophical thesis.** That thesis was **closed as a negative result by
  its own author** (it reduces to Nozick/Pettit/Sen; "reversibility" ≈ switching
  cost) — see the FDK `STATUS.md`. This repo is the *engineering* answer to "can the
  operational core run on a neutral runtime?" — yes, it can — not a revival of the
  closed philosophy.
- `coerced` / `deceived` are **declared inputs**, not detected. Detecting real
  coercion/deception from behaviour is unsolved and out of scope (the trust
  boundary).
- Divine Justice / Mahdavi are the policy's *objective*, represented as documented
  scorers — not a proof and not a world-optimizer.

*Theory: نظریه آزادی, Mohammad Ali Jannat Khah Doust (CC BY 4.0). Engineering:
Ali Pourrahim.*
