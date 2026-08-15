---
name: build-curl-impersonate-adapters
description: DRAFT/INACTIVE. Rebuild an authorized curl-impersonate source tree with a versioned browser/TLS profile overlay, package ABI-matched native libcurl and curl_cffi wrappers, and add a request-scoped compatibility adapter for curl_cffi and scrapy_cffi. Use when creating or updating a custom impersonation profile from owned captures, diagnosing a false Python/native integration, building Windows/Linux artifacts, or validating that custom and vendor profiles coexist without forking application code.
---

# Build curl-impersonate Adapters

## Status, authorization, and evidence

Treat this Skill as a draft until the workspace inventory marks it active. Work only with the user's own or
explicitly authorized traffic and endpoints. Do not use TLS fingerprint work to bypass access controls,
account restrictions, or third-party protections. Protocol resemblance is not browser identity and does not
prove that a client is undetectable.

Classify facts as `verified-repository`, `verified-official`, `verified-history`, `user-confirmed`, or
`hypothesis`. Use current official upstream documentation and source when selecting repositories, versions,
build commands, APIs, or supported targets. Historical values prove only the recorded candidates.

Never place packet captures, TLS key logs, cookies, authorization headers, private URLs, workstation paths,
tool installations, or raw decrypted requests in the Skill or public project documentation. Store sensitive
evidence in an ignored project-local directory and publish only bounded, redacted protocol facts.

## Fix the integration identity

Before editing, record:

- authoritative curl-impersonate repository URL and exact commit/tag;
- upstream curl/BoringSSL/nghttp2/ngtcp2/nghttp3 inputs selected by that revision;
- custom profile semantic name and native target name;
- capture browser version, OS/architecture, request type, protocol, and authorization basis;
- target OS, architecture, libc where applicable, Python implementation/ABI, and build toolchain;
- exact curl_cffi and optional scrapy_cffi versions and supported constraints;
- output mode: local candidate, installable wheel, native directory plus adapter, or release assets.

Keep product, protocol, and ABI identities independent. Do not infer wrapper compatibility from a matching
filename or library version string. Read [source-build-and-overlay.md](references/source-build-and-overlay.md)
for source locks, baseline builds, overlays, and platform toolchains.

## Select the integration route

1. **External native backend plus adapter (preferred)**: build an ABI-matched `_wrapper` against the custom
   dynamic libcurl, load it before curl_cffi, and map stable semantic profile names per request.
2. **Minimal curl_cffi fork/wheel**: use only when a self-contained distribution is required. Preserve the
   vendor Session/AsyncSession behavior and limit changes to native linking, target registration, packaging,
   and tests.
3. **Low-level Curl prototype**: use only to isolate whether the native target exists. It does not prove
   Session, async multi, cookies, redirects, callbacks, or scrapy_cffi integration.
4. **Runtime custom fingerprint API**: use only when the official API can express every required TLS/H2/H3
   field. Do not claim it is equivalent to a native profile when fields are missing.

Never overwrite an official target name with different bytes. Never make the custom profile a hidden global
default. Reject requests that pass both the semantic profile field and the vendor `impersonate` field.

Read [native-binding-and-packaging.md](references/native-binding-and-packaging.md) whenever linking, loading,
staging, or distributing native artifacts. Read
[python-adapter-contract.md](references/python-adapter-contract.md) for curl_cffi/scrapy_cffi integration.

## Build from a clean official baseline

Verify the clean upstream checkout and repository instructions first. Build the unmodified baseline, run its
feature/build checks, and record artifacts before adding a profile. Distinguish dependency-download failures,
compiler/toolchain failures, native profile failures, Python ABI failures, and live network failures.

Do not edit generated dependency sources as the durable solution. Follow repository policy for maintained
patches. When direct patch editing requires maintainer/user confirmation, use an idempotent overlay applied
after official patches and before compilation, then ask before converting it into the maintained patchset.
Fail if the insertion anchor or upstream source contract changed; never silently inject at a guessed location.

Treat the overlay, profile definition, upstream commit, toolchain, and every dependency lock as candidate
identity. Rebuild from a clean source/build directory before promotion.

## Extract and model an authorized profile

Read [capture-and-fingerprint-evidence.md](references/capture-and-fingerprint-evidence.md). Separate:

- stable ClientHello capabilities from GREASE values and randomized extension order;
- TLS facts from HTTP/2 SETTINGS/window/priority/pseudo-header order;
- HTTP/3 transport facts from HTTP/2 behavior;
- navigation headers from resource, prefetch, cached, authenticated, or protocol-specific headers;
- directly observed fields from values inherited from the nearest official baseline.

Do not hard-code cookies, session data, or one connection's GREASE/extension order. A capture without its
same-session TLS key log cannot prove encrypted HTTP/2/HTTP/3 headers or SETTINGS. A single JA3, JA4, Akamai
hash, User-Agent, or HTTP 200 response cannot prove profile fidelity.

## Build and bind the Python native layer

Build curl/libcurl first, then compile curl_cffi's wrapper against the exact installed headers and dynamic
library/import library. On Windows, distinguish the static `.lib` from the DLL import library. On Linux/macOS,
verify SONAME and loader path. Confirm the wrapper's actual imports with a platform tool; do not trust build
arguments alone.

The Python extension suffix must match the target interpreter ABI and platform. Stage the wrapper beside its
matching runtime library, hash both, and keep them one atomic backend generation. Loading a custom DLL next to
a wheel that statically embeds another libcurl is a false integration even if `ffi.dlopen()` succeeds.

## Add the request-scoped adapter

Activate the external wrapper before importing curl_cffi or scrapy_cffi. Make activation idempotent for the
same native directory and reject switching backend generations in one process. Retain Windows DLL-directory
handles. Preserve causes when the extension or adjacent library fails to load.

Keep a framework-owned registry mapping stable semantic names to native target strings. Unknown official
vendor targets may pass through only when that is the declared compatibility behavior. Wrap or inject
Session/AsyncSession rather than copying their connection, cookie, callback, WebSocket, or async lifecycle.
Keep scrapy_cffi optional and lazily imported; return its normal request type with only the resolved
`impersonate` value changed.

Do not let crawler defaults silently overwrite profile headers such as User-Agent. Resolve this explicitly in
project settings or the adapter contract.

## Validate by layers

Follow [validation-matrix.md](references/validation-matrix.md) and historical failures in
[verified-history-lessons.md](references/verified-history-lessons.md). At minimum verify:

1. clean upstream baseline build and feature list;
2. overlay idempotency and clean rebuild;
3. native CLI and direct `curl_easy_impersonate` target probe;
4. wrapper import table, ABI, adjacent-library resolution, and native version;
5. semantic custom profile, native custom name, an official profile, and no-profile request paths;
6. synchronous and asynchronous curl_cffi flows;
7. scrapy_cffi request mapping and one real downloader transport flow when supported;
8. clean-environment install on every declared platform/interpreter row;
9. artifact hashes, redaction scan, cleanup, and unsupported cells.

Record variable fingerprints rather than forcing a fixed JA3 assertion. Compare multiple protocol fields and
the capture-derived invariants. Classify transient checker/network failures before one bounded manual rerun;
never automatically retry programming, ABI, configuration, or unsupported-profile errors.

Create a project-local `curl-impersonate-integration.json` from
[integration-manifest.example.json](assets/integration-manifest.example.json), then run:

```powershell
python scripts/check_integration_readiness.py <project-root> --manifest curl-impersonate-integration.json
```

The checker validates portable paths, exact hashes, unique profile mappings, ABI declarations, and required
artifact roles. It does not prove runtime fingerprint fidelity.

## Finish

Report the locked source identity, observed versus inherited profile fields, artifact matrix, adapter route,
test levels, hashes, unsupported dimensions, sensitive evidence location class (never its private path), and
whether any package/release mutation occurred. Remove or ignore captures, key logs, build trees, venvs, caches,
and native artifacts that are not intentional deliverables.
