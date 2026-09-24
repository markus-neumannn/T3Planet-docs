# AGENTS.md — T3Planet Docs

## Production deployment

When the operator says **start the deployment process**, **start deployment**, **deploy latest docs**, or **push docs live**:

1. Follow [`.cursor/skills/t3planet-deploy/SKILL.md`](.cursor/skills/t3planet-deploy/SKILL.md).
2. Human SOP: [`docs/deployment/deploy.md`](docs/deployment/deploy.md).
3. Safety: [`.cursor/rules/deployment-safety.mdc`](.cursor/rules/deployment-safety.mdc) and [`.cursor/rules/mintlify-deployment.mdc`](.cursor/rules/mintlify-deployment.mdc).

**Never deploy** `docs-master/` or `workshops/`. Never force-push. Never claim success from GitHub push alone — verify Mintlify + live QA.

## Day-to-day docs

See repo `context.md` and `.cursor/rules/t3planet-client.mdc` for voice, paths (`TonicTypes/`), and local LAN preview (`:3000`).
