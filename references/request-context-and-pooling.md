# Request Context and Connection Pooling

## Separate the two identities

Model browser behavior on two independent axes:

```text
transport identity
  TLS ClientHello, ALPN, HTTP/2 or HTTP/3 settings, connection windows

request context
  navigation, fetch/XHR, subresource, preflight, form, WebSocket, and method/body semantics
```

A browser version does not have one universal header template. Fetch Metadata, Accept, Content-Type, Origin,
Referer, Priority, pseudo-header/ordinary-header order, and cache-related fields vary by request context. Keep
dynamic values such as cookies, authorization, content length, origin, referer, and conditional cache headers
out of static profile data unless the target project supplies them for that request.

## Declare the workload matrix first

Before capture or compilation, list the contexts the target application actually needs. At minimum distinguish
top-level navigation from programmatic fetch/XHR. When applicable, add same-origin and cross-origin fetch,
CORS preflight, script/style/image/font/media subresources, WebSocket handshake, JSON POST, and form submit.

For every required context, record:

- method/body and destination role;
- same-origin, same-site, or cross-site relationship;
- protocol and whether an existing connection was reused;
- observed Fetch Metadata, Accept, Origin/Referer, Priority, and header order;
- which values are stable, derived at request time, inherited, or unsupported.
- the exact native overlay or adapter preset that implements the context.

Pasting an API URL into an address bar still produces navigation semantics. Capture fetch/XHR from a real page
script or an equivalent authorized browser action. A reused HTTP/2 stream can prove request headers but does
not produce a new ClientHello; force a fresh authorized connection when transport comparison is required.

## Choose one context implementation route

Prefer native context variants when exact default-header insertion, deletion, or ordering matters:

```text
one native runtime
  browser-navigation
  browser-fetch-same-origin
  browser-fetch-cross-origin
  browser-subresource
```

Each variant may share transport fields while owning a distinct default-header contract. Compile every variant
into the same backend bundle.

Use one transport target plus adapter-owned context presets only when tests prove the native API can disable or
replace incompatible defaults and preserve exact ordering. The adapter must generate dynamic request fields,
not freeze captured values. Do not claim parity when merge/delete/order behavior is unknown.

Bind each manifest row to its implementation artifact: `native-profile` rows reference a manifest-listed
profile overlay, while `adapter-preset` rows reference a manifest-listed context preset. A name-to-target row
without that binding is registration metadata, not proof that the scenario was compiled or implemented.

## Bind connection pools to transport identity

TLS and HTTP/2/HTTP/3 connection state is established before later requests. Changing `impersonate` on a
request does not guarantee a new connection. A reused connection can otherwise combine one profile's
transport with another profile's headers.

Use a pool key that includes the resolved native target or an equally strict immutable transport identity in
addition to the framework's normal proxy, origin, certificate, and Session dimensions. Alternatively, bind a
Session to its first resolved target and reject later target changes. Different semantic aliases may share a
pool only when they resolve to the same proven transport identity.

## Validate scenario completeness

For each declared context:

1. Verify its semantic alias resolves to the intended native target or adapter preset.
2. Exercise a representative authorized request and inspect its actual headers and order.
3. Prove different native targets do not reuse one established connection pool.
4. Prove contexts sharing one transport identity retain correct per-request headers under safe reuse.
5. Mark absent scenarios unsupported; do not generalize from navigation or one successful response.
