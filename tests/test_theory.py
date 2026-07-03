"""The Theory of Freedom's axioms, as executable tests on the neutral kernel."""

from __future__ import annotations

import pytest

from dos_freedom import (
    Consent,
    ConsentLedger,
    FreedomGate,
    OwnershipError,
    OwnershipRegistry,
    valid_consent,
)

TOOLS = {
    "customer_db": lambda p: "read",
    "email": lambda p: "sent",
    "alice": lambda p: "SHOULD NEVER RUN",
}


def _world():
    r = OwnershipRegistry()
    r.register_person("alice")
    r.register_machine("bot", owner="alice")
    r.own_resource("alice", "customer_db")
    r.own_resource("alice", "email")
    r.delegate("alice", "bot", "customer_db")        # bot may act on customer_db only
    return r


# --- ownership axioms -------------------------------------------------------
def test_no_human_owns_another_and_machine_needs_owner():
    r = OwnershipRegistry()
    r.register_person("alice")
    with pytest.raises(OwnershipError):
        r.register_machine("bot", owner="bob")        # bob is not a person
    r.register_person("bob")
    with pytest.raises(OwnershipError):
        r.own_resource("bot", "x")                    # a non-person can't own


def test_cannot_delegate_a_resource_you_do_not_own():
    r = _world()
    r.register_person("mallory")
    r.own_resource("mallory", "secret_db")
    with pytest.raises(OwnershipError):
        r.delegate("alice", "bot", "secret_db")       # alice doesn't own it


# --- Freedom Verifier -------------------------------------------------------
def test_machine_may_not_act_upon_a_person(tmp_path):
    g = FreedomGate(_world(), ConsentLedger(), audit_path=str(tmp_path / "a.jsonl"))
    out = g.act("bot", {"resource": "alice"}, TOOLS)
    assert not out.executed and "machine_sovereignty" in out.reason


def test_action_outside_delegated_scope_is_forbidden(tmp_path):
    g = FreedomGate(_world(), ConsentLedger(), audit_path=str(tmp_path / "a.jsonl"))
    out = g.act("bot", {"resource": "email"}, TOOLS)   # email not delegated to bot
    assert not out.executed and "violates_property_rights" in out.reason


def test_delegated_action_is_permitted_and_executes(tmp_path):
    g = FreedomGate(_world(), ConsentLedger(), audit_path=str(tmp_path / "a.jsonl"))
    out = g.act("bot", {"resource": "customer_db", "nonce": "n1"}, TOOLS)
    assert out.executed and out.output == "read"


def test_coercion_and_deception_void_the_action(tmp_path):
    g = FreedomGate(_world(), ConsentLedger(), audit_path=str(tmp_path / "a.jsonl"))
    assert not g.act("bot", {"resource": "customer_db", "coerced": True}, TOOLS).executed
    assert not g.act("bot", {"resource": "customer_db", "deceived": True}, TOOLS).executed


# --- consent logic ----------------------------------------------------------
def test_valid_consent_predicate():
    ok = Consent(informed=True, voluntary=True, specific=True, revocable=True, competent=True)
    assert valid_consent(ok)
    assert not valid_consent(Consent(True, True, True, True, True, coerced=True))
    assert not valid_consent(Consent(True, True, True, True, competent=False))


def test_required_consent_must_be_valid(tmp_path):
    ledger = ConsentLedger()
    g = FreedomGate(_world(), ledger, audit_path=str(tmp_path / "a.jsonl"))
    act = {"resource": "customer_db", "nonce": "n2", "requires_consent_of": "alice"}
    assert not g.act("bot", act, TOOLS).executed             # no consent recorded
    ledger.record("alice", "n2",
                  Consent(informed=True, voluntary=True, specific=True, revocable=True, competent=True))
    assert g.act("bot", act, TOOLS).executed                 # now valid consent
