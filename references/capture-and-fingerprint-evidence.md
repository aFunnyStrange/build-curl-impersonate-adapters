# Capture and Fingerprint Evidence

## Sensitive capture boundary

Use only owned or authorized browsing sessions. Prefer a dedicated browser profile without accounts, cookies,
extensions, or unrelated tabs. TLS key logs can decrypt the matching captured sessions and must remain ignored,
local, access-restricted, and short-lived.

Setting `SSLKEYLOGFILE` after a connection was created cannot recover its secrets. Close all browser processes,
set the key-log destination, launch a dedicated profile, confirm the file grows, then capture new traffic. A
pcap and key log must come from the same session.

## What needs decryption

- Plain HTTP content: no TLS key log.
- ClientHello and most handshake-level TLS facts: normally no application-data decryption.
- HTTPS request/response headers and bodies: matching key log required.
- HTTP/2 SETTINGS, WINDOW_UPDATE, HEADERS, and DATA inside TLS: matching key log required.
- HTTP/3/QUIC request headers and application data: matching session secrets required.

Modern ECDHE usually prevents later decryption from the server certificate private key alone.

## Evidence model

Record browser version, OS, architecture, destination role, request type, negotiated protocol, frame/stream
identity, and whether each field was observed or inherited. Extract:

- ciphers, TLS versions, extensions, ALPN, groups, key shares, signature algorithms, compression, ALPS/ECH;
- GREASE and extension-permutation behavior rather than one randomized sequence;
- HTTP/2 SETTINGS, connection window update, priority, pseudo-header order, and ordinary header order;
- HTTP/3 transport parameters when claimed;
- navigation/resource/prefetch/cache differences and protocol-specific forbidden headers.

Treat address-bar navigation, link navigation, same-origin fetch/XHR, cross-origin fetch/XHR, preflight,
subresources, forms, and WebSocket handshakes as distinct evidence classes. An API-shaped URL opened as a
document remains navigation evidence. Record whether the stream reused a connection; header evidence from a
reused stream must not be presented as a newly observed TLS handshake.

Do not use a static-resource request as navigation evidence. Do not combine HTTP/1.1 navigation headers with
HTTP/2 resource behavior without declaring the approximation. If one profile structure cannot express
protocol/request-type variants, record the limitation instead of claiming exactness.

JA3 can vary when extension order is randomized. JA4 and HTTP/2/Akamai fingerprints are useful normalized
signals but are also reproducible and not identity proofs. Validate multiple connections and layers; do not
require every browser version to have a unique Akamai hash.
