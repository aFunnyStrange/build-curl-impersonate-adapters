# Failure Modes and Recovery Gates

Use this reference to diagnose integration failures without case-specific history. A recovery is complete only when the failed boundary is identified, the durable fix is applied at the correct layer, and the relevant validation gate passes again.

| Failure signature | Likely boundary | Required response and evidence |
| --- | --- | --- |
| A dependency edit disappears after a clean build | Generated dependency tree was edited directly | Move the change into a versioned patch, overlay, or build hook; rebuild from a clean checkout and prove the change is reapplied. |
| A capture exists but encrypted HTTP/2 or HTTP/3 fields cannot be inspected | No matching session key log was retained | Repeat the authorized capture with a matching session key log. Do not infer encrypted fields from another session. |
| Navigation headers, resource headers, or protocol versions differ | Evidence from different request classes was merged | Preserve request role and protocol as separate dimensions; compare only equivalent requests. |
| One JA3, JA4, or Akamai value matches | A partial fingerprint is being treated as an oracle | Require TLS, protocol, header, runtime-backend, package-content, and framework evidence. |
| Python accepts a profile name but behavior remains unchanged | Metadata support exists without native support | Trace the requested profile into the loaded native backend and verify observable wire behavior. |
| A wheel contains the intended wrapper but imports another runtime | Packaging and import resolution disagree | Inspect a clean installation, identify the loaded native module and runtime library, and fail closed on mismatches. |
| The linker rejects a plausible library file | Import, static, and runtime libraries were assigned the wrong roles | Classify artifacts by linker/runtime role and platform format; generate the correct artifact instead of renaming it. |
| A native build fails only under a wrapper or constrained shell | Tool discovery, environment propagation, or subprocess handling is broken | Discover toolchain programs explicitly, scope environment changes, preserve exit codes, and rebuild cleanly. |
| The external wrapper is activated after vendor imports | Backend selection happened too late | Activate it before vendor imports and expose the process-global backend identity for diagnostics. |
| Each Chrome profile produces its own wrapper/runtime directory | Profile identity was incorrectly treated as an ABI axis | Merge compatible overlays into one build and one native directory; keep request-time profile selection above the process-global backend. |
| A crawler accepts impersonation options but behavior is unchanged | Request mapping exists without a real transport bridge | Route requests through the adapted transport and prove direct and framework calls use the same backend. |
| A checker fails because an evidence endpoint is temporarily unavailable | External evidence dependency is unavailable | Use one bounded rerun or an approved equivalent; do not add unbounded retries or weaken unrelated gates. |

## Recovery discipline

1. Reproduce the smallest failing layer: source build, native wrapper, import selection, direct request, or framework transport.
2. Record source locks, build inputs, artifact hashes, runtime identity, and validation commands in the target project.
3. Fix the owning layer. Do not compensate above a lower-level contract that remains false.
4. Repeat the failed gate and all downstream gates affected by the change.
5. Keep fallbacks explicit, bounded, observable, and removable.

## Publication hygiene

Keep only reusable failure signatures and recovery rules in the Skill repository. Do not publish an originating task name, transcript, local filesystem layout, account name, private repository, captured traffic, cookies, tokens, or a narrative tied to one machine.
