# Native Binding and Packaging

## Artifact roles

Keep these roles explicit:

- curl-impersonate CLI: native smoke/debug entry;
- libcurl-impersonate runtime: owns profile implementation;
- static archive: embeds libcurl and usually requires transitive dependencies;
- import library: Windows link-time description of a DLL;
- curl_cffi wrapper: CPython/PyPy and platform-specific CFFI extension;
- adapter: Python-owned backend activation and request profile mapping;
- wheel or native directory: distribution container, not proof of compatibility.

Hash the final staged bytes, not only build outputs. One wrapper/runtime-library pair plus one shared profile
manifest is an atomic backend generation and must bind upstream commit, curl_cffi source revision, Python ABI,
OS, architecture, compiler, and the complete ordered profile-overlay set.

## Mandatory bundle cardinality

For each declared platform/architecture/Python-ABI axis, package exactly one native directory containing:

- one ABI-matched curl_cffi wrapper;
- one adjacent libcurl-impersonate runtime, plus unavoidable platform symlinks when applicable;
- one manifest listing every semantic alias and compiled native target;
- licenses and integrity metadata required by the distribution.

Compile all compatible Chrome and other browser profiles into that runtime. Never emit one directory, wrapper,
runtime library, wheel, or archive per profile. Profile selection belongs to each request; native-directory
selection belongs to process startup. Separate bundles are valid only for different platform/architecture/ABI
axes, not for browser versions or aliases.

The manifest must also bind each alias to a request context, header strategy, and transport identity. Several
context variants may share transport fields or even one native target, but they remain explicit validation
rows rather than one falsely universal browser profile. Bind every row to its hashed native overlay or adapter
preset artifact so declared coverage cannot exceed packaged implementation.

## Prove the loaded backend

Use platform inspection (`dumpbin`, `llvm-objdump`, `objdump`, `readelf`, `otool`, or equivalent) to prove the
wrapper imports the intended dynamic library. At runtime record:

- extension file path and suffix;
- resolved native directory without publishing private roots;
- native curl version/features;
- direct custom and official profile probe results;
- artifact SHA-256 values.

Do not accept these false positives:

- Python profile-name validation passes but native probe returns unsupported;
- custom DLL loads through ctypes/CFFI while Session still calls a statically embedded libcurl;
- editable fork is accidentally imported instead of the installed official Python layer;
- one same-named DLL earlier on PATH wins loader resolution;
- wrapper and runtime library came from different builds.
- two profile-specific directories are required for requests sharing one target axis.

## Package choices

For a native-directory plus adapter distribution, keep the vendor Python package installed normally and
activate the external wrapper before import. For a self-contained wheel, include the ABI-matched wrapper and
runtime library, preserve licenses/notices, and test the built wheel in a clean environment.

Never call a platform-specific wheel universal. Build and test every declared Python ABI, OS, architecture,
and libc target, but keep all compatible profiles consolidated inside each target's single bundle. Keep debug
symbols and private build paths out of public native binaries or apply reproducible prefix maps before
qualification.
