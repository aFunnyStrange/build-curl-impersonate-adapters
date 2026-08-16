---
name: build-curl-impersonate-adapters
description: DRAFT/INACTIVE. Rebuild an authorized curl-impersonate source tree with versioned browser/TLS profile overlays, compile compatible transport and request-context profiles into one ABI-matched native backend bundle per target, and add a connection-safe compatibility adapter for curl_cffi and scrapy_cffi. Use when creating custom impersonation behavior from owned captures, separating navigation, fetch/XHR, subresource, preflight, or WebSocket scenarios, diagnosing false Python/native integration or connection reuse, building Windows/Linux artifacts, or validating that profiles coexist behind one native directory without forking application code.
---

# Build curl-impersonate Adapters

## Status, authorization, and evidence

Treat this Skill as a draft until the workspace inventory marks it active. Work only with the user's own or
explicitly authorized traffic and endpoints. Do not use TLS fingerprint work to bypass access controls,
account restrictions, or third-party protections. Protocol resemblance is not browser identity and does not
prove that a client is undetectable.

Classify facts as `verified-repository`, `verified-official`, `user-confirmed`, or `hypothesis`. Use current
official upstream documentation and source when selecting repositories, versions, build commands, APIs, or
supported targets. Revalidate every source revision, platform, ABI, package version, and runtime claim in the
current project.

Never place task titles or transcripts, usernames, machine paths, hostnames, packet captures, TLS key logs,
cookies, authorization headers, credentials, private URLs, tool installations, or raw decrypted requests in
the Skill or public project documentation. Store sensitive evidence in an ignored project-local directory and
publish only reusable workflow rules and bounded, redacted protocol facts.

## Fix the integration identity

Before editing, record:

- authoritative curl-impersonate repository URL and exact commit/tag;
- upstream curl/BoringSSL/nghttp2/ngtcp2/nghttp3 inputs selected by that revision;
- the complete requested profile set, with each semantic name and native target name;
- the required request-context matrix and which scenarios are intentionally unsupported;
- capture browser version, OS/architecture, request type, protocol, and authorization basis;
- target OS, architecture, libc where applicable, Python implementation/ABI, and build toolchain;
- exact curl_cffi and optional scrapy_cffi versions and supported constraints;
- output mode: local candidate, installable wheel, native directory plus adapter, or release assets.

Keep product, protocol, and ABI identities independent. Do not infer wrapper compatibility from a matching
filename or library version string. Read [source-build-and-overlay.md](references/source-build-and-overlay.md)
for source locks, baseline builds, overlays, and platform toolchains.

## Enforce one backend bundle per target

Treat `OS + architecture + libc/toolchain boundary + Python ABI` as the native artifact axis. Profile names are
not artifact axes. For each target axis, apply every compatible official and custom profile overlay in one
source build and package exactly one `_wrapper`, one adjacent libcurl runtime, and one profile manifest in one
native directory.

Do not build or package one wrapper/runtime directory per Chrome version, site variant, or semantic alias. Do
not make curl_cffi or scrapy_cffi select native directories per request. Activate one directory once per
process; select one compiled native target per request through `impersonate` or a semantic alias. If requested
profiles cannot coexist in one runtime, fail and report the native conflict instead of silently shipping
profile-sharded backends.

Keep transport identity separate from request context. A browser-family/version transport can support several
navigation, fetch/XHR, subresource, preflight, form, or WebSocket scenarios whose headers and ordering differ.
Read [request-context-and-pooling.md](references/request-context-and-pooling.md) before declaring profile
coverage or designing Session reuse.

## Select the integration route

1. **External native backend plus adapter (preferred)**: build one ABI-matched `_wrapper` against the shared
   multi-profile dynamic libcurl, load one native directory before curl_cffi, bulk-register semantic mappings,
   and select a compiled profile per request.
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

Treat the ordered profile set, every overlay, upstream commit, toolchain, and dependency lock as one candidate
identity. Apply the whole profile set before compilation and rebuild it from one clean source/build directory
before promotion. Bind every declared request-context row to a hashed native overlay or adapter preset included
in the candidate manifest; an alias alone is not implementation evidence.

## Extract and model an authorized profile

Read [capture-and-fingerprint-evidence.md](references/capture-and-fingerprint-evidence.md). Separate:

- stable ClientHello capabilities from GREASE values and randomized extension order;
- TLS facts from HTTP/2 SETTINGS/window/priority/pseudo-header order;
- HTTP/3 transport facts from HTTP/2 behavior;
- navigation headers from resource, prefetch, cached, authenticated, or protocol-specific headers;
- directly observed fields from values inherited from the nearest official baseline.

Do not hard-code cookies, session data, or one connection's GREASE/extension order. Do not label a navigation
capture as a generic API/fetch profile merely because the response is JSON. A capture without its
same-session TLS key log cannot prove encrypted HTTP/2/HTTP/3 headers or SETTINGS. A single JA3, JA4, Akamai
hash, User-Agent, or HTTP 200 response cannot prove profile fidelity.

## Build and bind the Python native layer

Build curl/libcurl first, then compile curl_cffi's wrapper against the exact installed headers and dynamic
library/import library. On Windows, distinguish the static `.lib` from the DLL import library. On Linux/macOS,
verify SONAME and loader path. Confirm the wrapper's actual imports with a platform tool; do not trust build
arguments alone.

The Python extension suffix must match the target interpreter ABI and platform. Stage the sole wrapper beside
its sole matching runtime library and shared profile manifest, hash them, and keep them as one atomic
multi-profile backend generation. Loading a custom DLL next to a wheel that statically embeds another libcurl
is a false integration even if `ffi.dlopen()` succeeds.

## Add the request-scoped adapter

Activate the external wrapper before importing curl_cffi or scrapy_cffi. Make activation idempotent for the
same native directory and reject switching backend generations in one process. Retain Windows DLL-directory
handles. Preserve causes when the extension or adjacent library fails to load.

Load one manifest and bulk-register its semantic-name-to-native-target mappings during native activation. Keep
a framework-owned registry mapping stable semantic names to native target strings. Unknown official vendor
targets may pass through only when that is the declared compatibility behavior. Wrap or inject
Session/AsyncSession rather than copying their connection, cookie, callback, WebSocket, or async lifecycle.
Keep scrapy_cffi optional and lazily imported; return its normal request type with only the resolved
`impersonate` value changed.

Do not let crawler defaults silently overwrite profile headers such as User-Agent. Resolve this explicitly in
project settings or the adapter contract.

Bind every reusable connection pool to one resolved native transport/profile identity. Include that identity
in the Session/pool cache key, or reject attempts to change it after the Session establishes a connection. Do
not assume a per-request `impersonate` change creates a new TLS connection. Request contexts may share a pool
only when they resolve to the same transport identity and vary headers without changing connection-level
behavior.

## Validate by layers

Follow [validation-matrix.md](references/validation-matrix.md) and generic recovery gates in
[failure-modes.md](references/failure-modes.md). At minimum verify:

1. clean upstream baseline build and feature list;
2. overlay idempotency and clean rebuild;
3. native CLI and direct `curl_easy_impersonate` target probe;
4. wrapper import table, ABI, adjacent-library resolution, and native version;
5. every declared request context, multiple custom native names, an official profile, and the no-profile path
   through the same native directory and process;
6. synchronous and asynchronous curl_cffi flows;
7. connection-pool isolation for different resolved native targets and safe reuse for the same transport;
8. scrapy_cffi request-context mapping and one real downloader transport flow per required scenario;
9. clean-environment install on every declared platform/interpreter row;
10. exactly one wrapper/runtime pair and one shared profile manifest for each target axis;
11. artifact hashes, redaction scan, cleanup, and unsupported cells.

Record variable fingerprints rather than forcing a fixed JA3 assertion. Compare multiple protocol fields and
the capture-derived invariants. Classify transient checker/network failures before one bounded manual rerun;
never automatically retry programming, ABI, configuration, or unsupported-profile errors.

Create a project-local `curl-impersonate-integration.json` from
[integration-manifest.example.json](assets/integration-manifest.example.json), then run:

```powershell
python scripts/check_integration_readiness.py <project-root> --manifest curl-impersonate-integration.json
```

The checker validates portable paths, exact hashes, unique profile mappings, ABI declarations, one bundle
directory and exact bundle-role cardinality per target axis. It does not prove runtime fingerprint fidelity.

## Finish

Report the locked source identity, observed versus inherited profile fields, artifact matrix, adapter route,
test levels, hashes, unsupported dimensions, sensitive evidence location class (never its private path), and
whether any package/release mutation occurred. Remove or ignore captures, key logs, build trees, venvs, caches,
and native artifacts that are not intentional deliverables.
