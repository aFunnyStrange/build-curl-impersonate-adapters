# Source Build and Profile Overlay

## Lock and baseline

Use the current authoritative upstream repository selected by the user/project. Verify its remote, exact
commit, submodules or downloaded dependency locks, license, repository instructions, and supported build
targets. Current source layout and commands are unstable facts; confirm them from official documentation and
the checked-out revision.

Build the unmodified source first. Record the compiler, generator, SDK/sysroot, architecture, dependency
features, install prefix, and hashes. A custom profile build is uninterpretable when the official baseline did
not pass on the same host.

Keep build and install directories disposable and separate from editable overlay inputs. Do not preserve a
successful change only inside `build/**/deps/src/...`; a clean build will erase it.

## Overlay contract

Prefer an idempotent overlay when repository policy forbids or gates direct edits to maintained patchsets. The
overlay should:

- run after official patches and before compilation;
- verify the exact source file and a stable insertion anchor;
- detect an already-present target and exit successfully;
- fail closed when the target name conflicts or the anchor changes;
- inject a standalone, reviewable profile fragment;
- be included in the candidate hash/manifest.

After proving the candidate, follow the repository's maintainer workflow to convert or integrate the change.
Do not edit a protected patch file without the required user/maintainer confirmation.

## Windows lessons

- Enter the intended Visual Studio developer environment explicitly; a normal PowerShell may not expose
  compiler, linker, CMake generator, or Windows SDK tools.
- Limit ExecutionPolicy changes to the current process when required.
- Verify `rc.exe` can actually start in the child build environment. If a local extension safely omits an
  embedded manifest, scope `/MANIFEST:NO` only to that custom local mode rather than changing official builds.
- Propagate subprocess non-zero exit codes; PowerShell does not turn every native failure into an exception.
- Never hard-code a workstation-specific Visual Studio path in reusable scripts. Discover supported instances
  or accept an explicit parameter.

The DLL import library can be much smaller than a static library. Link the wrapper to the import library when
the intended package uses a neighboring DLL; choosing the static archive may require every transitive library
and can accidentally embed a second backend.

## Linux/WSL/macOS lessons

- Use the platform's native compiler and a venv; do not mix Windows build tools into WSL/Linux.
- Keep large intermediate builds on a native filesystem when mounted-drive performance or semantics are poor.
- Respect PEP 668 and avoid `--break-system-packages` for a build environment.
- Verify `RPATH`/`RUNPATH`, SONAME, libc baseline, architecture, and extension suffix.
- Quote nested shell variables carefully when a host shell launches WSL or another shell.

## Rebuild gate

Promotion requires a clean build from the locked source plus overlay, not only an incremental re-link of a
generated source tree. Compare the clean outputs with the candidate manifest and rerun native/Python tests.
