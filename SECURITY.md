# Security Policy

## Scope

Motion Site Builder is a library of prompts, Markdown references, and a small
suite of **zero-dependency Python** tools (a motion linter, a corpus indexer,
and an MCP server that speaks JSON-RPC over stdio). It ships no runtime service,
handles no user data, and requires no credentials. The attack surface is
correspondingly small, but we take it seriously.

Realistic concerns we care about:

- The MCP server or linter mishandling untrusted input (a malformed file path,
  a hostile code string passed to `motion_validate`, a crafted JSON-RPC frame)
  in a way that reads outside the repo, hangs, or executes unintended code.
- The `build_index.py` corpus scanner following a path it shouldn't.
- A supply-chain issue in the landing page under `site/` (its npm
  dependencies), even though it is a static demo.

Out of scope: the aesthetic quality of generated sites, licensed media source
pages recorded for provenance (direct third-party asset hotlinks are not
shipped; downloaded files remain the user's responsibility), and issues in AI
builders (Bolt, Lovable, v0, Cursor) that consume the prompts.

## Reporting a Vulnerability

Please **do not open a public issue** for a security problem.

Use GitHub's private advisory flow:
**[Report a vulnerability](https://github.com/olbboy/motion-site-builder/security/advisories/new)**
(Security → Advisories → *Report a vulnerability* on the repository).

Include, where you can: affected file or tool, a minimal reproduction, the
observed vs. expected behavior, and any suggested fix. A proof-of-concept that
stays within your own environment is welcome.

## What to Expect

- **Acknowledgement** within 5 business days.
- An initial assessment (severity, scope, whether it's in scope) shortly after.
- A fix or mitigation for confirmed, in-scope issues, and credit in the release
  notes if you'd like it.

Because this is a small open-source project maintained on a best-effort basis,
timelines are targets, not guarantees. Thank you for helping keep it safe.

## Supported Versions

The latest release on `main` is the only supported version. Fixes land there
and ship in the next tagged release.
