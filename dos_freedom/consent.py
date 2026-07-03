"""Consent Logic — valid_consent, exactly as the theory specifies.

    valid_consent(H, A) :- informed, voluntary, specific, revocable, competent,
                           not coerced, not deceived.
    invalid_consent(H, A) :- coerced ; deceived.

Honest boundary (documented, not hidden): `coerced` / `deceived` are *declared*
inputs. Detecting real coercion/deception from behaviour is unsolved and out of
scope — this encodes the RULE, not a coercion detector. That gap is on the trust
boundary (see the FDK STATUS 'attested → detected gap').
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Consent:
    informed: bool
    voluntary: bool
    specific: bool
    revocable: bool
    competent: bool
    coerced: bool = False
    deceived: bool = False


def valid_consent(c: Consent) -> bool:
    return (
        c.informed
        and c.voluntary
        and c.specific
        and c.revocable
        and c.competent
        and not c.coerced
        and not c.deceived
    )


class ConsentLedger:
    def __init__(self) -> None:
        self._by_ref: dict[tuple[str, str], Consent] = {}

    def record(self, human: str, action_ref: str, consent: Consent) -> None:
        self._by_ref[(human, action_ref)] = consent

    def is_valid(self, human: str, action_ref: str) -> bool:
        c = self._by_ref.get((human, action_ref))
        return c is not None and valid_consent(c)
