# Verified Historical Task Lessons

## Evidence scope

These lessons come from the retrieved task **学习 curl-impersonate TLS 封装** and the corresponding local
repository/toolchain artifacts. They describe one custom browser-profile experiment across Windows and WSL;
they are not current upstream compatibility guarantees.

## Durable lessons

- Start with the official profile closest to the observed browser capabilities, then encode only proven
  differences. The experiment inherited uncertain values explicitly instead of pretending the capture proved
  them.
- Editing the expanded curl dependency tree enabled a fast prototype but vanished after cleaning. An
  idempotent CMake overlay applied after upstream patches made the candidate rebuildable without violating the
  repository rule that patch edits required user confirmation.
- The first capture lacked same-session TLS secrets, so it could prove ClientHello fields but not encrypted
  HTTP/2 SETTINGS or header order. A new dedicated-browser capture plus key log exposed those fields and also
  revealed sensitive authenticated cookies, reinforcing strict local-only handling.
- One navigation used HTTP/1.1 while static resources used HTTP/2. A single generic header table could not fully
  represent request-type and protocol differences; the result documented that approximation.
- JA3 varied under GREASE/extension permutation. JA4 could also vary with an observed extension-count variant,
  and two browser profiles could share one Akamai hash. No single hash became the success oracle.
- Adding the custom target to a Python whitelist did not prove integration. The installed Windows curl_cffi
  wheel embedded its own libcurl, so separately loading the custom DLL left high-level requests on another
  backend.
- Rebuilding the wrapper against the custom DLL closed that gap. On Windows, the small DLL import library—not
  the larger static archive—was the correct input. Import-table inspection and native profile probes proved the
  binding.
- Windows builds encountered missing/inaccessible `rc.exe`, nested shell environment loss, and native commands
  whose non-zero status was not automatically raised by PowerShell. The final local-only extension build
  scoped `/MANIFEST:NO` and explicitly checked exit codes.
- The final adapter loaded the external wrapper before vendor imports, kept activation process-global and
  idempotent, retained the DLL-directory handle, mapped a semantic name per request, preserved official
  profiles, and rejected ambiguous dual profile arguments.
- curl_cffi synchronous/async paths and scrapy_cffi request plus real transport paths passed in clean
  environments on two platform/Python ABI rows. Import paths were checked to exclude an editable-fork false
  positive.
- A TLS checker closed one connection transiently; one unchanged rerun passed. The workflow did not add a
  general automatic retry for programming or configuration failures.

## Privacy and portability

The historical repository included workstation paths, build-tool locations, captures, key logs, native
binaries, and version-specific names. None belongs in this Skill. Preserve only portable roles, relative-path
examples, redacted protocol values when truly reusable, and the evidence distinctions above.
