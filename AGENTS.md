# Agent Instructions

## Do not read `.secrets/`

`.secrets/` holds this machine's real credentials and the generated,
ready-to-deploy cloud-init file — see [docs/secrets.md](docs/secrets.md).
Do not read, list, grep, or otherwise inspect the contents of `.secrets/`
(`.secrets/credentials.yaml`, `.secrets/cloud-init.yaml`) unless the user
explicitly asks you to for that specific file, in that specific turn.

This applies even to:
- Broad codebase searches/greps that would otherwise match it
- "Understand the project" / exploration tasks
- Debugging `build.py` (reason about it from `templates/*.tmpl.yaml` and
  `templates/credentials.example.yaml` instead of the real files)

If you need to confirm the build works, run `build.py` and check its exit
code/permissions output — don't cat the resulting file.
