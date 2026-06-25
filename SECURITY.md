# Security Policy

## Supported Versions

Only the latest release version receives security updates.

| Version | Supported          |
| ------- | ------------------ |
| v1.0.x  | :white_check_mark: |
| < v1.0  | :x:                |

## Reporting a Vulnerability

We take the security of Altair AI seriously. If you find a security vulnerability, please do **NOT** report it publicly via a GitHub issue. Instead, follow these steps:

1. Send an email to **deonbinny7@gmail.com** explaining the vulnerability.
2. Include a detailed description of the exploit vector, steps to reproduce, and a proof of concept (PoC) if available.
3. We will acknowledge receipt of your report within 48 hours and coordinate a fix.
4. Once resolved, we will release a security patch and credit you for the disclosure (unless requested otherwise).

## Handling of Secrets & Keys

* **Never commit API keys, private passwords, or certificates to Git.**
* Use the provided `.env.example` to define necessary variables, and place real values inside a local, gitignored `.env` file.
* If a secret is accidentally committed to Git, immediately revoke it, delete the remote branch, and rotate the credential.
