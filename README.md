# Build curl-impersonate Adapters

> Status: **draft-inactive**. The workflow was distilled from one retrieved real project task and repository,
> but still needs an independent forward use and explicit activation approval.

This Skill rebuilds an authorized curl-impersonate source tree with a custom TLS/H2/H3 profile and integrates
the resulting native backend with curl_cffi and optional scrapy_cffi. It focuses on reproducible source locks,
idempotent profile overlays, ABI-matched wrapper/runtime pairs, request-scoped profile selection, and layered
validation that detects false Python/native integrations.

It deliberately excludes captures, TLS key logs, cookies, private URLs, workstation paths, and historical
native binaries. Those remain private project evidence. The Skill records only portable workflows and
sanitized failure lessons.

## Install for Codex

Do not install this draft until it is activated. After activation, link the complete source directory into the
user Skill directory; do not copy editable sources.

Windows PowerShell:

```powershell
$skillsRoot = Join-Path $HOME ".agents\skills"
$source = (Resolve-Path "<repository-root>\build-curl-impersonate-adapters").Path
$link = Join-Path $skillsRoot "build-curl-impersonate-adapters"
New-Item -ItemType Directory -Force -Path $skillsRoot | Out-Null
if (Test-Path -LiteralPath $link) { throw "Destination already exists: $link" }
New-Item -ItemType Junction -Path $link -Target $source | Out-Null
```

macOS:

```bash
skills_root="$HOME/.agents/skills"
source_dir="$(cd "<repository-root>/build-curl-impersonate-adapters" && pwd)"
link_path="$skills_root/build-curl-impersonate-adapters"
mkdir -p "$skills_root"
if [ -e "$link_path" ] || [ -L "$link_path" ]; then echo "Destination already exists: $link_path" >&2; exit 1; fi
ln -s "$source_dir" "$link_path"
```

After activation, invoke it as `$build-curl-impersonate-adapters`. CC Switch v3.13 or newer may import the
linked local Skill for compatible agents, but each agent's file format, tools, permissions, and native build
environment must still be reviewed.

## Resources

- `SKILL.md`: core source, build, adapter, privacy, and qualification workflow.
- `references/`: source overlay, capture evidence, native packaging, Python adapter, validation, and retrieved
  historical lessons.
- `assets/integration-manifest.example.json`: portable artifact/evidence manifest template.
- `scripts/check_integration_readiness.py`: read-only manifest, path, role, ABI-pair, and SHA-256 checker.
