# Security

## Private vulnerability reports

Do not open a public issue for a vulnerability in the compiler, the stile
example, or the generated output.

Report privately with the repository advisory form:

https://github.com/the-homestead-hub/hubwik/security/advisories/new

You may also write to hello@thehomesteadhub.co.uk with the subject
`HubWīk security`.

Please include:

- a description of the issue
- steps that demonstrate it in this repository or in generated `dist/`
- the impact you expect

We will acknowledge the report and say when you can expect a further reply.

## What is in scope

- The compiler writing secrets, credentials, or merchant identifiers into
  `dist/`
- Path traversal or unexpected file writes when compiling a malicious record
- The stile example leaking a settlement address or wallet (it must not have
  one)
- Dependency or workflow abuse in this repository

## What is out of scope

- A live shop theme, checkout, or till. Those are private overlays.
- Settlement, facilitators, production stile hostnames, and wallets. Those
  are a separate private service.
- Content accuracy that is not a safety claim. Use a crop-correction issue.
- Safety-affecting growing or eating advice. Use [docs/SAFETY.md](docs/SAFETY.md)
  and the crop-correction form.

## Public workflows

Pull-request workflows run with read-only permissions, no repository secrets,
and no deployment. Do not add `pull_request_target` or publish from a public
fork pull request.
