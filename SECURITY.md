# Security Policy

## Scope and status

`freedom-policy` implements the Theory of Freedom as **policy** on the
value-neutral `decision-os-min` kernel; the kernel is not modified. The theory
content here is a **research artifact / injected policy** — it answers "should
this happen at all?" and may only DENY; it never grants authority. Any
comparative claim against existing approaches (e.g. RLHF / CAI / OPA) is
**unproven** and framed as such in the docs.

This project has **not** had an independent third-party security audit. The
security properties of the underlying kernel are governed by that kernel's own
policy; this repository only adds refusal logic on top. Do not treat this policy
layer as a hardened security boundary without your own review.

## Supported versions

This is pre-1.0 software. Only the latest commit on the default branch receives
security fixes. There are no long-term-support branches.

## Reporting a vulnerability

Please report suspected vulnerabilities **privately** — do not open a public
issue for anything exploitable.

- Preferred: open a private report via GitHub Security Advisories
  ("Report a vulnerability" under the repository's **Security** tab).
- Alternatively, email the maintainer: **nikzadpars@gmail.com**.

Please include:

- a description of the issue and the affected component/file,
- reproduction steps or a proof of concept,
- the impact you believe it has, and
- any suggested remediation.

## Disclosure process

- We aim to acknowledge a report within **7 days**.
- We aim to provide an initial assessment (accepted / needs-info / not-a-vuln)
  within **30 days**.
- We follow **coordinated disclosure**: please give us a reasonable window to
  ship a fix before any public disclosure. We will credit reporters who wish to
  be credited.

## No bounty

There is no paid bug-bounty program. Reports are handled on a best-effort basis
by the maintainer.
