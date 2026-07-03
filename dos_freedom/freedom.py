"""Freedom Verifier + Justice/Guidance/Mahdavi objective + the full pipeline.

Implements the theory's execution structure on the value-neutral decision-os-min
kernel (the kernel is NOT modified — the whole theory lives here as policy):

    Ownership Resolution -> Consent Verification -> Freedom Verifier
      -> Kernel (authorization) -> Runtime Guard (PEP) -> Execution -> Audit

Freedom Verifier (the theory's forbidden/permissible core):
    forbidden(A) :- violates_property_rights | coerces | deceives
                    | machine_sovereignty | bypasses_verifier.
    permissible(A) :- action(A), not(forbidden(A)).

Honest split: ownership / consent / the forbidden-rules are RUNNABLE. The
DivineJustice, Guidance and Mahdavi functions are the theory's *objective* — they
are value functions, represented here as explicit, documented scorers, NOT proven
world-optimizers. They advise; they never grant.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from .consent import ConsentLedger
from .ownership import OwnershipRegistry


@dataclass
class FreedomOutcome:
    permitted: bool
    executed: bool
    reason: str
    output: Any = None


def build_policy(registry: OwnershipRegistry) -> dict[str, Any]:
    """Derive a kernel policy from ownership: a machine's granted capabilities are
    exactly the resources explicitly delegated to it (MachineScope ⊆ owner scope).
    Nothing else. Default-deny."""
    grants: dict[str, list[str]] = {}
    for machine in registry._machines:  # noqa: SLF001 — reading the registry we own
        grants[machine] = [f"tool:{r}" for r in sorted(registry.delegated(machine))]
    return {"grants": grants, "default": "deny"}


# --- Divine Justice / Guidance / Mahdavi: the OBJECTIVE (value functions) -----
def divine_justice_ok(rights_violation: bool) -> bool:
    """DivineJustice(a) := maximize Justice s.t. NoRightsViolation. The *constraint*
    is runnable (no action that violates rights is just); the 'maximize' is the
    policy's stated objective, not an optimizer over the world."""
    return not rights_violation


def mahdavi_score(reduces_violation: bool, increases_coercion: bool) -> float:
    """MahdaviCompass: does the action move toward universal non-violation? A
    documented heuristic (advisory), not a proof."""
    return (1.0 if reduces_violation else 0.0) - (0.5 if increases_coercion else 0.0)


def guidance_valid(preserves_rights: bool, reduces_conflict: bool, preserves_verifier: bool) -> bool:
    """GuidanceFunction: a rule revision is valid iff it preserves rights + the
    verifier and reduces conflict — never revolution against the axioms."""
    return preserves_rights and reduces_conflict and preserves_verifier


class FreedomGate:
    """Runs the theory's pipeline. Holds no authority of its own — the kernel
    decides; this gate only refuses actions the theory forbids *before* the kernel,
    and lets the kernel + PEP enforce the rest."""

    def __init__(self, registry: OwnershipRegistry, consent: ConsentLedger, *, audit_path: str) -> None:
        from decision_os_min import DecisionOS  # the value-neutral runtime

        self.registry = registry
        self.consent = consent
        self._dos = DecisionOS(build_policy(registry), audit_path=audit_path)

    def _freedom_verify(self, machine: str, action: dict[str, Any]) -> str | None:
        """The Freedom Verifier: return a 'forbidden' reason, or None if permissible."""
        target = action.get("resource") or action.get("target")
        # machine_sovereignty: a machine may never act to own/subjugate a person.
        if target is not None and self.registry.is_person(target):
            return "machine_sovereignty: a machine may not act upon a person"
        # coerces / deceives (declared inputs — see consent.py honesty note).
        if action.get("coerced"):
            return "coercion: consent obtained under coercion is void"
        if action.get("deceived"):
            return "deception: consent obtained by deception is void"
        # violates_property_rights: acting on a resource not delegated within scope.
        if target is not None and not self.registry.may_act_on(machine, target):
            return f"violates_property_rights: '{machine}' has no delegated right over '{target}'"
        # consent, when required, must be valid.
        req = action.get("requires_consent_of")
        if req is not None and not self.consent.is_valid(req, action.get("nonce", "")):
            return f"invalid_or_absent_consent from '{req}'"
        return None

    def act(
        self,
        machine: str,
        action: dict[str, Any],
        tools: dict[str, Callable[[dict[str, Any]], Any]],
    ) -> FreedomOutcome:
        forbidden = self._freedom_verify(machine, action)
        if forbidden is not None:
            return FreedomOutcome(permitted=False, executed=False, reason=forbidden)

        # Permissible under the theory -> hand to the neutral kernel for
        # authorization + mandatory-mediation execution + audit.
        target = action.get("resource") or action.get("target") or action.get("tool", "")
        kernel_action = {
            "actor": machine,
            "tool": target,
            "capability": f"tool:{target}",
            "action_purpose": action.get("action_purpose", ""),
            "data_labels": list(action.get("data_labels", [])),
            "payload": action.get("payload", {}),
            "nonce": action.get("nonce", ""),
        }
        out = self._dos.handle(kernel_action, tools)
        return FreedomOutcome(
            permitted=out.executed or out.verdict in ("ALLOW", "LIMIT", "CONTAIN"),
            executed=out.executed,
            reason=out.refused_reason or out.verdict,
            output=out.output,
        )
