# Security Swarm (Agentes de seguridad)

Este repositorio es un proyecto de ejemplo configurado para que Devin ejecute un **Security Swarm** propio: un enjambre de subagentes especializados que modelan amenazas, escanean código, validan exploits y escriben parches.

## Cómo se usa

Desde cualquier sesión de Devin en este repositorio, pide:

```
Run the security swarm on the sample app. Find vulnerabilities, validate the exploitable ones in the sandbox, and open remediation PRs with regression tests.
```

Devin descubrirá los perfiles en `.devin/agents/` y podrá lanzar los subagentes en paralelo siguiendo el flujo descrito en este archivo.

## Flujo del enjambre

1. **Threat modeler** — construye un modelo de amenazas: entry points, activos sensibles, superficies de ataque y perfiles de atacante.
2. **Scanner** — uno o varios subagentes escanean rutas de código, razonan sobre flujos de datos y buscan inyecciones, bypass de auth, path traversal, SSRF, secretos expuestos, etc.
3. **Validator** — reproduce cada hallazgo de alta confianza en el sandbox local (construye y ejecuta la app de forma segura), confirmando exploitabilidad.
4. **Remediator** — escribe el parche mínimo, agrega un test de regresión, ejecuta la suite y resume el cambio para PR.

## Prompts de ejemplo

Ver `PROMPTS.md`.
