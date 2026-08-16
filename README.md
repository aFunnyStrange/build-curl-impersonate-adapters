# Build curl-impersonate Adapters

> Status: **draft-inactive**. This public Skill contains only reusable workflow contracts, validation gates,
> and generic examples. It still needs an independent forward use and explicit activation approval.

This Skill rebuilds an authorized curl-impersonate source tree with a custom TLS/H2/H3 profile and integrates
the resulting native backend with curl_cffi and optional scrapy_cffi. It focuses on reproducible source locks,
idempotent multi-profile overlays, exactly one ABI-matched backend bundle per target, request-scoped profile
selection through one native directory, and layered validation that detects false Python/native integrations.

For one platform, architecture, and Python ABI, every compatible browser profile must be compiled into one
runtime and packaged as one wrapper/runtime/manifest directory. curl_cffi and scrapy_cffi configure that one
directory at process startup and select profiles per request; profile-specific native packages are rejected.

Completeness is workload-specific: navigation, fetch/XHR, subresources, preflight, forms, and WebSocket
handshakes are separate request contexts rather than one universal browser header template. The manifest must
declare required contexts and their coverage. Connection pools must remain bound to one resolved native
transport/profile so a later request cannot reuse an incompatible TLS connection.

It deliberately excludes captures, TLS key logs, cookies, private URLs, credentials, task transcripts,
workstation paths, and native binaries. The Skill records only portable workflows and generic failure gates.

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
- `references/`: source overlay, request-context/pooling, capture evidence, native packaging, Python adapter,
  validation, and generic failure/recovery gates.
- `assets/integration-manifest.example.json`: portable artifact/evidence manifest template.
- `scripts/check_integration_readiness.py`: read-only manifest, path, single-bundle cardinality, ABI, and
  SHA-256 checker.
