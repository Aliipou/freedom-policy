"""Conflict resolution DERIVED from the theory's axioms — beyond 'defer-to-human'.

The theory resolves conflict by *ownership clarification*, never by sacrificing a
right. Its axioms give a ladder the current implementations don't fully use:

  1. INALIENABLE PRIMACY — a person's body / mind / consent / **data about them**
     are inalienably theirs (data ∈ individual property rights). Anyone else's claim
     on that resource is *derived*, not primary.
  2. CONSENT SCOPE — a derived claim is valid ONLY within the consent the inalienable
     owner granted (specific + revocable). Outside scope, the derived claim is void.
  3. REVERSIBILITY PREFERENCE — when two INALIENABLE claims genuinely collide, prefer
     the reversible action; never commit an irreversible rights-violation while
     resolving.
  4. DIVINE-JUSTICE CONSTRAINT — never resolve by sacrificing a right.
  5. DEADLOCK → HUMAN — only genuine inalienable-vs-inalienable ties survive to here.

Honest residual: step 1 needs data PROVENANCE ("who is the inalienable owner of this
datum") — the attested→detected gap — and true ties still need a human.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Resolution(Enum):
    A_WINS = "a_wins"
    B_WINS = "b_wins"
    BOTH_WITHIN_CONSENT = "both_permitted_within_consent"
    DEADLOCK_HUMAN = "deadlock_human_arbitration"


@dataclass(frozen=True)
class Claim:
    who: str
    resource: str
    inalienable_owner: bool          # is `who` the inalienable owner of `resource`?
    within_consent_scope: bool = False   # (for a derived claim) granted by the owner, in scope?
    reversible: bool = True


@dataclass(frozen=True)
class ResolutionResult:
    resolution: Resolution
    reason: str

    @property
    def resolved(self) -> bool:
        return self.resolution is not Resolution.DEADLOCK_HUMAN


def resolve(a: Claim, b: Claim) -> ResolutionResult:
    # 1+2. Exactly one is the inalienable owner -> primacy, bounded by consent scope.
    if a.inalienable_owner != b.inalienable_owner:
        owner, derived = (a, b) if a.inalienable_owner else (b, a)
        owner_wins = Resolution.A_WINS if owner is a else Resolution.B_WINS
        if derived.within_consent_scope:
            return ResolutionResult(
                Resolution.BOTH_WITHIN_CONSENT,
                f"'{derived.who}' acts within consent '{owner.who}' granted on "
                f"'{owner.resource}'; no rights violated.",
            )
        return ResolutionResult(
            owner_wins,
            f"inalienable primacy: '{owner.who}' owns '{owner.resource}'; "
            f"'{derived.who}''s derived claim is outside consent scope and is void.",
        )

    # 3. Two INALIENABLE claims collide -> prefer the reversible; never commit the
    #    irreversible rights-violation while resolving.
    if a.inalienable_owner and b.inalienable_owner:
        if a.reversible and not b.reversible:
            return ResolutionResult(
                Resolution.A_WINS,
                "reversibility preference: 'a' is reversible, 'b' is not",
            )
        if b.reversible and not a.reversible:
            return ResolutionResult(
                Resolution.B_WINS,
                "reversibility preference: 'b' is reversible, 'a' is not",
            )
        # 4+5. Both reversible or both irreversible -> no principled winner without
        #      sacrificing a right -> human, never a rights violation.
        return ResolutionResult(
            Resolution.DEADLOCK_HUMAN,
            "two inalienable claims, equal reversibility: human arbitration; no right sacrificed.",
        )

    # Neither is an inalienable owner (two derived claims) -> deadlock to human.
    return ResolutionResult(
        Resolution.DEADLOCK_HUMAN, "two derived claims, no inalienable primacy: human arbitration."
    )
