# Python Adapter Contract

## Native activation

The adapter must accept exactly one native directory for the process and load its external extension as the
module name expected by curl_cffi before any curl_cffi or scrapy_cffi import. It must:

- locate only the current interpreter's supported extension suffix;
- reject a missing or ambiguous wrapper;
- add and retain a Windows DLL-directory handle when needed;
- remove a partially inserted module after load failure;
- preserve the original exception as the cause;
- return the same activation record for the same directory;
- reject a second backend directory in the same process.

Do not unload and swap native backends in a running process. Use a new process for another generation. Never
choose a native directory from the request's profile name.

## Profile registry

Own a stable semantic profile name separately from the native target name. Resolve at request time:

```text
semantic profile -> registered native target
vendor impersonate name -> declared pass-through
neither -> no implicit profile
both -> configuration error
```

Load all mappings from the bundle's manifest during one-time activation. Registration does not select a
default and must not be repeated per request. Never shadow an official name with different behavior.

Each mapping must declare its transport identity, request context, and header strategy. Resolve those fields
before selecting a Session or pool. Keep context presets separate from native-target aliases even when both
are exposed through one convenience API.

## Session and pool identity

Do not use one connection pool across different resolved native targets merely because requests share a host.
Key cached Sessions/pools by the resolved native target or an equivalent immutable transport identity, in
addition to the framework's existing proxy/origin/certificate dimensions. If the framework cannot expose a
safe pool key, bind a Session to the first target and reject a later change.

Multiple request contexts may reuse one pool only when they share the same proven transport identity and the
adapter changes request headers without switching connection-level behavior. Test this boundary with reused
HTTP/2 or HTTP/3 connections; a successful response alone is insufficient.

## curl_cffi composition

Wrap or inject the vendor `Session` and `AsyncSession`; do not reimplement connection pooling, cookies,
redirects, callbacks, WebSockets, async multi, or error models. Close injected versus owned sessions according
to an explicit ownership contract. Keep vendor version checks at construction/activation rather than every
request when capabilities are stable.

If the installed curl_cffi version changes its private target-registration logic, prefer the public API or a
small version adapter. Treat reliance on a private global set as a prototype, not a stable release contract.

## scrapy_cffi composition

Keep scrapy_cffi an optional import. Build its normal request type and set only the resolved `impersonate`
field plus an explicitly supported request-context preset when applicable. Verify the downloader transport
uses the activated wrapper and a profile-safe pool; request-object mapping alone is not enough. Check crawler
settings that can overwrite browser headers, especially User-Agent. Do not fork the scheduler or downloader
when a normal public request/transport seam is sufficient.
