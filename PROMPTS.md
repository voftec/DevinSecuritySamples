# Prompts de ejemplo para el Security Swarm

## 1. Escaneo completo

```
Run the security swarm on the sample app. Find all high-confidence vulnerabilities, validate the exploitable ones in the local sandbox, and open remediation PRs with regression tests.
```

## 2. Modelado de amenazas

```
Spawn the threat-modeler subagent. Build a concise threat model for the sample-app/ directory and report the top 5 risk areas.
```

## 3. Scanner dirigido

```
Spawn the scanner subagent focused on auth bypass and injection vulnerabilities in sample-app/app.py. Include file paths, line numbers, and confidence levels.
```

## 4. Validación de un hallazgo

```
Validator: reproduce the SQL injection in /login using the running sample app. Confirm the exploit, show the request/response, and report steps.
```

## 5. Remediación

```
Remediator: fix the validated SQL injection in sample-app/app.py, add a regression test, run the test suite, and summarize the PR.
```

## 6. Custom Security Swarm

```
Use the custom subagents in .devin/agents/ to run a full security review of this repo. First model threats, then scan, then validate, then remediate.
```
