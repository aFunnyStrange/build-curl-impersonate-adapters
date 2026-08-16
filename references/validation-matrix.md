# Validation Matrix

## Gates

| Gate | Required evidence |
| --- | --- |
| Source | remote, exact commit/tag, clean state, dependency locks, license |
| Baseline | official build, feature check, native request/probe |
| Overlay | all requested profiles applied together, anchor verification, idempotency, clean rebuild, profile-set hash |
| Native | one runtime exposes every custom/official target; CLI probes and TLS/H2/H3 fields as claimed |
| Binding | exactly one wrapper/runtime pair per target axis, shared directory, ABI suffix, loader path, native version |
| Adapter unit | one-directory activation, bulk alias mapping, pass-through, conflict, no default, import-order rejection |
| curl_cffi | sync/async profile switching in one process and Session, custom semantic/native, official, plain, cleanup |
| scrapy_cffi | normal request mapping plus real transport request and close |
| Distribution | one consolidated multi-profile bundle for every declared OS/Python/arch/libc row; clean install |
| Privacy | no captures, key logs, cookies, tokens, private URLs/paths, build caches |

Separate deterministic checks from live network evidence. One TLS checker may close a connection or return a
different hash without proving the candidate broken. Retain the error, compare another authorized endpoint or
one bounded rerun, and classify DNS/proxy/VPN/firewall/remote-service failures separately.

For fingerprint validation, require profile probe success, expected browser-family/version header fields,
declared TLS capabilities, negotiated protocol, capture-derived H2/H3 parameters, and agreement between
semantic alias and native target. Record variable JA3/JA4 values; assert only invariants justified by multiple
captures or current official baselines.

After tests, close sessions/transports, remove temporary venv/build/native staging, and retain only intentional
manifest-bound artifacts. Do not publish until the exact clean-installed artifacts pass.
