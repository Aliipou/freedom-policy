"""The derived conflict-resolution ladder, on the canonical hard cases.

The point: cases the theory's axioms actually settle are RESOLVED here (not
deferred). Only genuine inalienable-vs-inalienable ties survive to a human.
"""

from __future__ import annotations

from dos_freedom.conflict import Claim, Resolution, resolve


def test_cannot_sell_a_persons_data_inalienable_primacy():
    # Alice (business) holds data ABOUT Bob and wants to SELL it — outside any
    # consent Bob gave. Bob inalienably owns his own data.
    alice = Claim("alice", "bob_personal_data", inalienable_owner=False, within_consent_scope=False)
    bob = Claim("bob", "bob_personal_data", inalienable_owner=True)
    r = resolve(alice, bob)
    assert r.resolution is Resolution.B_WINS and r.resolved      # Bob wins — RESOLVED, not deferred
    assert "inalienable primacy" in r.reason


def test_within_consent_scope_is_reconciled_not_a_conflict():
    # Bob granted Alice access for support. Using it for support = within scope.
    alice = Claim("alice", "bob_personal_data", inalienable_owner=False, within_consent_scope=True)
    bob = Claim("bob", "bob_personal_data", inalienable_owner=True)
    r = resolve(alice, bob)
    assert r.resolution is Resolution.BOTH_WITHIN_CONSENT and r.resolved


def test_two_inalienable_claims_reversibility_preference():
    # Two people, colliding actions; one reversible, one not -> permit the reversible.
    a = Claim("carol", "shared_doc", inalienable_owner=True, reversible=True)
    b = Claim("dave", "shared_doc", inalienable_owner=True, reversible=False)
    r = resolve(a, b)
    assert r.resolution is Resolution.A_WINS      # reversible one proceeds; nothing irreversible done
    assert "reversibility" in r.reason


def test_genuine_tie_defers_to_human_without_sacrificing_a_right():
    a = Claim("carol", "shared_doc", inalienable_owner=True, reversible=False)
    b = Claim("dave", "shared_doc", inalienable_owner=True, reversible=False)
    r = resolve(a, b)
    assert r.resolution is Resolution.DEADLOCK_HUMAN and not r.resolved
    assert "no right sacrificed" in r.reason
