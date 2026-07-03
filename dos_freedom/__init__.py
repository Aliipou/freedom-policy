"""dos_freedom — the Theory of Freedom's OPERATIONAL core, implemented on the
value-neutral decision-os-min kernel.

    Rights Ontology + Ownership Registry   (ownership.py)   — RUNNABLE
    Consent Logic                          (consent.py)     — RUNNABLE
    Freedom Verifier (forbidden/permissible)(freedom.py)    — RUNNABLE
    Divine Justice / Guidance / Mahdavi     (freedom.py)    — value functions, advisory

The kernel is NOT modified: the theory is expressed entirely as policy + a
pre-kernel verifier. This implements the theory's *executable* structure; it does
not claim the theory's philosophical thesis (which its own author closed as a
negative result — see the FDK STATUS).
"""

from __future__ import annotations

from .conflict import Claim, Resolution, ResolutionResult, resolve
from .consent import Consent, ConsentLedger, valid_consent
from .freedom import (
    FreedomGate,
    FreedomOutcome,
    build_policy,
    divine_justice_ok,
    guidance_valid,
    mahdavi_score,
)
from .ownership import OwnershipError, OwnershipRegistry

__all__ = [
    "OwnershipRegistry",
    "OwnershipError",
    "Consent",
    "ConsentLedger",
    "valid_consent",
    "Claim",
    "Resolution",
    "ResolutionResult",
    "resolve",
    "FreedomGate",
    "FreedomOutcome",
    "build_policy",
    "divine_justice_ok",
    "guidance_valid",
    "mahdavi_score",
]
