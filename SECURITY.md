# Security Policy

## Supported Versions

This project is under continuous autonomous development. Only the latest commit
on the default branch is actively supported.

| Version        | Supported          |
|----------------|--------------------|
| default branch | :white_check_mark: |

## Reporting a Vulnerability

Please do **not** open a public issue for security vulnerabilities. Instead,
open a private report using GitHub's "Report a vulnerability" feature on the
repository's **Security** tab, or contact the maintainers directly.

Please include:

- The affected file and line(s) if known
- A description of the vulnerability and its potential impact
- Steps to reproduce, if applicable

You can expect an acknowledgement within 7 days. If the vulnerability is
confirmed, a fix will be prioritized and a public advisory will be published
when appropriate.

## Security Considerations for This Project

This repository is an autonomous AI agent that runs on GitHub Actions with
write access to the repository. Treat `opencode.json` and
`.github/workflows/*.yml` as security-sensitive configuration:

- Secrets are stored as GitHub Actions secrets, never in the repository.
- `GITHUB_TOKEN` permissions are scoped to the minimum required.
- Validation for workflow and configuration files runs in `.github/workflows/ci.yml`.