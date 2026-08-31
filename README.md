# DevinSecuritySamples

Proyecto de ejemplo y agentes custom para el workshop **Programación Agéntica con Devin AI para Seguridad Informática**.

## Qué incluye

- `sample-app/` — aplicación Flask intencionalmente vulnerable para practicar escaneos y remediación.
- `.devin/agents/` — perfiles de subagentes especializados (`threat-modeler`, `scanner`, `validator`, `remediator`).
- `AGENTS.md` — instrucciones del enjambre (swarm workflow).
- `PROMPTS.md` — prompts de ejemplo.
- `.devin/blueprint.yaml` — entorno Devin preconfigurado.

## Cómo usar en Devin

1. Clona el repo en una sesión de Devin Cloud / Desktop.
2. Pide a Devin: 
   ```
   Run the security swarm on the sample app.
   ```
3. Devin cargará los perfiles de `.devin/agents/` y ejecutará el flujo de modelado → escaneo → validación → remediación.

## Documentación oficial

- Security Swarm: https://docs.devin.ai/work-with-devin/security-swarm
- Subagents: https://docs.devin.ai/cli/subagents
- Blueprints: https://docs.devin.ai/onboard-devin/environment/blueprint-reference

## Nota de seguridad

La aplicación de ejemplo es deliberadamente insegura y solo debe usarse en entornos aislados de aprendizaje.
