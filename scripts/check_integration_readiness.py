"""Validate a curl-impersonate integration manifest and artifact hashes."""

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple


SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
REQUIRED_ROLES = {"profile-overlay", "native-wrapper", "runtime-library"}


def sha256_file(path: Path) -> str:
    """Return the lowercase SHA-256 digest for one file."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest(path: Path) -> Dict[str, Any]:
    """Load one JSON object from disk."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest root must be a JSON object")
    return value


def portable_path(root: Path, value: Any) -> Tuple[Optional[Path], Optional[str]]:
    """Resolve a portable project-relative path without allowing escape."""
    if not isinstance(value, str) or not value.strip():
        return None, "artifact path must be a non-empty string"
    candidate = Path(value)
    if candidate.is_absolute() or candidate.drive:
        return None, f"artifact path must be relative: {value}"
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        return None, f"artifact path escapes project root: {value}"
    return resolved, None


def audit_manifest(root: Path, manifest: Dict[str, Any]) -> List[str]:
    """Return readiness errors without changing the project."""
    errors: List[str] = []
    if manifest.get("schemaVersion") != 1:
        errors.append("schemaVersion must equal 1")

    source = manifest.get("source")
    if not isinstance(source, dict):
        errors.append("source must be an object")
    else:
        repository = source.get("repository")
        if not isinstance(repository, str) or not repository.startswith("https://"):
            errors.append("source.repository must be an HTTPS URL")
        commit = source.get("commit")
        if not isinstance(commit, str) or not COMMIT_PATTERN.fullmatch(commit):
            errors.append("source.commit must be a lowercase 40-character Git commit")

    python_config = manifest.get("python")
    if not isinstance(python_config, dict) or not python_config.get("curlCffi"):
        errors.append("python.curlCffi must record the tested version/constraint")

    profiles = manifest.get("profiles")
    seen_semantic: Set[str] = set()
    if not isinstance(profiles, list) or not profiles:
        errors.append("profiles must contain at least one mapping")
    else:
        for index, profile in enumerate(profiles):
            if not isinstance(profile, dict):
                errors.append(f"profiles[{index}] must be an object")
                continue
            semantic = profile.get("semanticName")
            native = profile.get("nativeTarget")
            if not isinstance(semantic, str) or not semantic.strip():
                errors.append(f"profiles[{index}].semanticName is required")
            elif semantic in seen_semantic:
                errors.append(f"duplicate semantic profile: {semantic}")
            else:
                seen_semantic.add(semantic)
            if not isinstance(native, str) or not native.strip():
                errors.append(f"profiles[{index}].nativeTarget is required")

    artifacts = manifest.get("artifacts")
    roles: Set[str] = set()
    native_pairs: Set[Tuple[str, str, str]] = set()
    runtime_pairs: Set[Tuple[str, str, str]] = set()
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("artifacts must contain manifest-bound files")
        return errors

    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            errors.append(f"artifacts[{index}] must be an object")
            continue
        role = artifact.get("role")
        if not isinstance(role, str) or not role:
            errors.append(f"artifacts[{index}].role is required")
            continue
        roles.add(role)
        path, path_error = portable_path(root, artifact.get("path"))
        if path_error is not None:
            errors.append(f"artifacts[{index}]: {path_error}")
        elif path is not None and not path.is_file():
            errors.append(f"artifacts[{index}] does not exist: {artifact.get('path')}")

        expected = artifact.get("sha256")
        if not isinstance(expected, str) or not SHA256_PATTERN.fullmatch(expected):
            errors.append(f"artifacts[{index}].sha256 must be lowercase SHA-256")
        elif path is not None and path.is_file():
            actual = sha256_file(path)
            if actual != expected:
                errors.append(
                    f"artifacts[{index}] hash mismatch: expected {expected}, got {actual}"
                )

        if role in {"native-wrapper", "runtime-library"}:
            platform = artifact.get("platform")
            python_abi = artifact.get("pythonAbi")
            if not isinstance(platform, str) or not platform:
                errors.append(f"artifacts[{index}].platform is required for {role}")
            if not isinstance(python_abi, str) or not python_abi:
                errors.append(f"artifacts[{index}].pythonAbi is required for {role}")
            if isinstance(platform, str) and isinstance(python_abi, str):
                key = (platform, python_abi, role)
                if role == "native-wrapper":
                    native_pairs.add(key)
                else:
                    runtime_pairs.add(key)

    missing_roles = REQUIRED_ROLES - roles
    for role in sorted(missing_roles):
        errors.append(f"missing required artifact role: {role}")

    wrapper_axes = {(platform, abi) for platform, abi, _ in native_pairs}
    runtime_axes = {(platform, abi) for platform, abi, _ in runtime_pairs}
    for axis in sorted(wrapper_axes - runtime_axes):
        errors.append(f"native wrapper has no runtime-library pair: {axis[0]}/{axis[1]}")
    for axis in sorted(runtime_axes - wrapper_axes):
        errors.append(f"runtime library has no native-wrapper pair: {axis[0]}/{axis[1]}")
    return errors


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", type=Path)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("curl-impersonate-integration.json"),
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run the read-only readiness check."""
    args = build_parser().parse_args(argv)
    root = args.project_root.resolve()
    manifest_path = args.manifest
    if not manifest_path.is_absolute():
        manifest_path = root / manifest_path
    try:
        manifest = load_manifest(manifest_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: unable to load manifest: {exc}")
        return 1
    errors = audit_manifest(root, manifest)
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"Integration readiness failed with {len(errors)} error(s).")
        return 1
    print("Integration manifest and artifact hashes are ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
