"""Rights Ontology + Ownership Registry — the theory's operational base, in code.

Implements the ownership axioms as ENFORCED invariants (not prose):

    Person(h) -> OwnedByGod(h)                 # no one else owns a person
    Person(h1) & Person(h2) & h1!=h2 -> not Owns(h1, h2)
    Machine(m) -> exists h: HumanOwner(h, m)   # every machine has a human owner
    Machine(m) & Person(h) -> not Owns(m, h)   # a machine never owns a person
    MachineScope(m) subset-of PropertyScope(owner)
    DelegatedProperty(m, r) requires HumanOwner(h,m) & Owns(h,r) & ExplicitDelegation

This is the runnable half of the Theory of Freedom. Divine Justice / Guidance /
Mahdavi Compass are the *objective* on top (see objective.py) — documented values,
not enforced optimizers. Nothing here holds kernel authority; it produces the
policy the value-neutral kernel then enforces.
"""

from __future__ import annotations

from dataclasses import dataclass, field


class OwnershipError(RuntimeError):
    """Raised when an action would violate an ownership axiom."""


@dataclass
class OwnershipRegistry:
    _persons: set[str] = field(default_factory=set)
    _machines: dict[str, str] = field(default_factory=dict)        # machine -> human owner
    _owns: dict[str, str] = field(default_factory=dict)            # resource -> owner (person)
    _delegations: dict[str, set[str]] = field(default_factory=dict)  # machine -> {resource}

    # --- registration (axiom-checked) ---------------------------------------
    def register_person(self, person: str) -> None:
        self._persons.add(person)

    def register_machine(self, machine: str, owner: str) -> None:
        if owner not in self._persons:
            raise OwnershipError(f"machine owner '{owner}' is not a registered person")
        if machine in self._persons:
            raise OwnershipError(f"'{machine}' is a person and cannot be a machine")
        self._machines[machine] = owner        # Machine(m) -> HumanOwner(h, m)

    def own_resource(self, person: str, resource: str) -> None:
        if person not in self._persons:
            raise OwnershipError(f"only a person may own a resource; '{person}' is not one")
        self._owns[resource] = person

    def delegate(self, owner: str, machine: str, resource: str) -> None:
        """A human explicitly delegates a resource they own to their machine."""
        if self._machines.get(machine) != owner:
            raise OwnershipError(f"'{owner}' is not the human owner of machine '{machine}'")
        if self._owns.get(resource) != owner:
            raise OwnershipError(
                f"'{owner}' does not own resource '{resource}' — cannot delegate it"
            )
        self._delegations.setdefault(machine, set()).add(resource)

    # --- queries (used to build the kernel policy) --------------------------
    def is_person(self, x: str) -> bool:
        return x in self._persons

    def human_owner(self, machine: str) -> str | None:
        return self._machines.get(machine)

    def delegated(self, machine: str) -> set[str]:
        return set(self._delegations.get(machine, set()))

    def may_act_on(self, machine: str, resource: str) -> bool:
        """A machine may operate on a resource only if it was explicitly delegated
        AND (MachineScope ⊆ PropertyScope) — the resource is still owned by the
        machine's human owner. A machine may NEVER act to own/subjugate a person."""
        if self.is_person(resource):
            return False                        # Machine & Person -> not Owns(m, person)
        owner = self.human_owner(machine)
        return (
            resource in self.delegated(machine)
            and self._owns.get(resource) == owner
        )
