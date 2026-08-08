#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Shared, dependency-free helpers for repository automation.

Metadata files with a ``.yaml`` suffix are deliberately JSON-compatible YAML.
This keeps CI bootstrapping deterministic and avoids executing or importing data.
"""

from __future__ import annotations

import contextlib
import datetime as dt
import errno
import fcntl
import gzip
import hashlib
import io
import json
import os
import pathlib
import re
import shutil
import stat
import tarfile
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Iterable, Iterator, List, Mapping, MutableMapping, Optional, Sequence, Tuple


SCHEMA_VERSION = 1
USER_AGENT = "openeuler-riscv-packages/1.0 (+https://github.com/yinjiayi/openeuler-riscv-packages)"
SAFE_ID = re.compile(r"^[a-z0-9](?:[a-z0-9._+-]{0,126}[a-z0-9])?$")
HEX_SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")


class ToolError(Exception):
    """An expected input, policy, or operational failure."""

    def __init__(self, message: str, exit_code: int = 2) -> None:
        super().__init__(message)
        self.exit_code = exit_code


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def isoformat(value: dt.datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=dt.timezone.utc)
    return value.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_time(value: Any) -> Optional[dt.datetime]:
    if value in (None, "", 0, "0"):
        return None
    if isinstance(value, (int, float)):
        return dt.datetime.fromtimestamp(float(value), tz=dt.timezone.utc)
    text = str(value).strip()
    if text.isdigit():
        return dt.datetime.fromtimestamp(float(text), tz=dt.timezone.utc)
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = dt.datetime.fromisoformat(text)
    except ValueError as exc:
        raise ToolError("invalid timestamp: %s" % value) from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def parse_now(value: Optional[str]) -> dt.datetime:
    return parse_time(value) if value else utc_now()  # type: ignore[return-value]


def stable_json(data: Any, pretty: bool = True) -> str:
    if pretty:
        return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _reject_unsafe_yaml(text: str, origin: str) -> None:
    stripped = text.lstrip()
    if stripped.startswith(("---", "%YAML", "!!", "!<")):
        raise ToolError(
            "%s is not JSON-compatible YAML; convert it to JSON syntax before use" % origin
        )


def loads_document(text: str, origin: str = "input") -> Any:
    _reject_unsafe_yaml(text, origin)
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ToolError("%s must contain JSON-compatible YAML: %s" % (origin, exc)) from exc


def load_json(path: os.PathLike[str] | str, default: Any = None) -> Any:
    source = pathlib.Path(path)
    if not source.exists():
        if default is not None:
            return default
        raise ToolError("file does not exist: %s" % source)
    try:
        return loads_document(source.read_text(encoding="utf-8"), str(source))
    except OSError as exc:
        raise ToolError("cannot read %s: %s" % (source, exc), 1) from exc


def atomic_write(path: os.PathLike[str] | str, content: bytes, mode: int = 0o644) -> None:
    destination = pathlib.Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".%s." % destination.name, dir=str(destination.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, destination)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def atomic_write_text(path: os.PathLike[str] | str, content: str, mode: int = 0o644) -> None:
    atomic_write(path, content.encode("utf-8"), mode)


def atomic_write_json(path: os.PathLike[str] | str, data: Any, mode: int = 0o644) -> None:
    atomic_write_text(path, stable_json(data), mode)


def emit_json(data: Any, output: Optional[str] = None) -> None:
    if output:
        atomic_write_json(output, data)
    else:
        print(stable_json(data), end="")


def slugify(value: Any, max_length: int = 96) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"[^a-z0-9._+-]+", "-", text)
    text = re.sub(r"[-_.+]{2,}", "-", text).strip("-._+")
    if not text:
        raise ToolError("cannot derive a safe identifier from %r" % value)
    text = text[:max_length].rstrip("-._+")
    if not SAFE_ID.match(text):
        raise ToolError("unsafe identifier: %s" % text)
    return text


def package_identifier(value: Any, max_length: int = 100) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", str(value or "").strip().lower()).strip("-")
    text = re.sub(r"-{2,}", "-", text)[:max_length].rstrip("-")
    if not text or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", text):
        raise ToolError("cannot derive a schema-valid package id from %r" % value)
    return text


def ensure_within(root: pathlib.Path, candidate: pathlib.Path) -> pathlib.Path:
    resolved_root = root.resolve()
    resolved = candidate.resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise ToolError("path escapes allowed root: %s" % candidate) from exc
    return resolved


def safe_one_line(value: Any, field: str, max_length: int = 512) -> str:
    text = str(value or "").strip()
    if not text:
        raise ToolError("missing %s" % field)
    if "\n" in text or "\r" in text or "\x00" in text:
        raise ToolError("%s must be a single line" % field)
    if len(text) > max_length:
        raise ToolError("%s is too long" % field)
    return text


def validate_https_url(value: str, allow_file: bool = False, allow_fixture: bool = False) -> str:
    parsed = urllib.parse.urlsplit(value)
    allowed = {"https"}
    if allow_file:
        allowed.add("file")
    if allow_fixture:
        allowed.add("fixture")
    if parsed.scheme not in allowed:
        raise ToolError("URL must use an allowed scheme (%s): %s" % (", ".join(sorted(allowed)), value))
    if parsed.scheme == "https" and not parsed.hostname:
        raise ToolError("URL has no host: %s" % value)
    if parsed.username or parsed.password:
        raise ToolError("credentials in URLs are forbidden")
    return value


def canonical_url(value: Any) -> Optional[str]:
    if not value:
        return None
    text = str(value).strip()
    try:
        parsed = urllib.parse.urlsplit(text)
    except ValueError:
        return None
    if parsed.scheme not in ("https", "http") or not parsed.hostname:
        return None
    host = parsed.hostname.lower().rstrip(".")
    if host.startswith("www."):
        host = host[4:]
    path = re.sub(r"/{2,}", "/", parsed.path).rstrip("/")
    path = re.sub(r"\.git$", "", path, flags=re.IGNORECASE)
    for marker in ("/releases/tag/", "/releases/download/", "/archive/refs/tags/", "/-/archive/"):
        if marker in path:
            path = path.split(marker, 1)[0]
    if host in {"github.com", "gitlab.com", "codeberg.org"}:
        parts = [part for part in path.split("/") if part]
        path = "/" + "/".join(parts[:2])
    return urllib.parse.urlunsplit(("https", host, path, "", ""))


def release_component_key(record: Mapping[str, Any]) -> Optional[str]:
    upstream = record.get("upstream") if isinstance(record.get("upstream"), Mapping) else {}
    values = [
        upstream.get("repository_url"),
        upstream.get("homepage"),
        record.get("upstream_url"),
        record.get("homepage"),
        record.get("source_url"),
    ]
    for value in values:
        canonical = canonical_url(value)
        if not canonical:
            continue
        parsed = urllib.parse.urlsplit(canonical)
        if parsed.hostname in {"aur.archlinux.org", "archlinux.org"}:
            continue
        identity = "%s%s" % (parsed.hostname, parsed.path.lower())
        return slugify(identity.replace("/", "-"), max_length=126)
    return None


def get_nested(data: Mapping[str, Any], *keys: str, default: Any = None) -> Any:
    current: Any = data
    for key in keys:
        if not isinstance(current, Mapping) or key not in current:
            return default
        current = current[key]
    return current


def first_value(data: Mapping[str, Any], names: Sequence[str], default: Any = None) -> Any:
    for name in names:
        if name in data and data[name] not in (None, ""):
            return data[name]
    return default


def as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def version_key(value: Any) -> Tuple[Any, ...]:
    text = str(value or "").strip().lstrip("vV")
    parts = re.findall(r"\d+|[A-Za-z]+", text)
    key: List[Tuple[int, Any]] = []
    pre = {"dev": -5, "snapshot": -4, "alpha": -3, "a": -3, "beta": -2, "b": -2, "rc": -1}
    for part in parts:
        if part.isdigit():
            key.append((2, int(part)))
        else:
            lowered = part.lower()
            key.append((0 if lowered in pre else 1, pre.get(lowered, lowered)))
    return tuple(key)


def is_prerelease(record: Mapping[str, Any]) -> bool:
    if bool(record.get("prerelease")) or bool(record.get("draft")):
        return True
    version = str(first_value(record, ["version", "tag_name", "name"], ""))
    return bool(re.search(r"(?:^|[._-])(alpha|beta|rc|pre|preview|dev|snapshot|nightly)(?:[._-]|\d|$)", version, re.I))


def iter_records(document: Any) -> List[Mapping[str, Any]]:
    if isinstance(document, list):
        return [item for item in document if isinstance(item, Mapping)]
    if not isinstance(document, Mapping):
        raise ToolError("metadata root must be an object or array")
    for key in ("candidates", "packages", "results", "components", "items", "releases"):
        value = document.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, Mapping)]
    if any(key in document for key in ("name", "Name", "package_id", "version", "Version")):
        return [document]
    return []


class HostRateLimiter:
    def __init__(self, requests_per_second: float = 2.0) -> None:
        if requests_per_second <= 0:
            raise ToolError("requests-per-second must be positive")
        self.interval = 1.0 / requests_per_second
        self.last: Dict[str, float] = {}

    def wait(self, host: str) -> None:
        now = time.monotonic()
        delay = self.interval - (now - self.last.get(host, 0.0))
        if delay > 0:
            time.sleep(delay)
        self.last[host] = time.monotonic()


def fetch_url(
    url: str,
    *,
    timeout: float = 30.0,
    retries: int = 3,
    cache_dir: Optional[pathlib.Path] = None,
    limiter: Optional[HostRateLimiter] = None,
    max_bytes: int = 2 * 1024 * 1024 * 1024,
) -> Tuple[bytes, Dict[str, Any]]:
    validate_https_url(url, allow_file=True)
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme == "file":
        path = pathlib.Path(urllib.request.url2pathname(parsed.path))
        data = path.read_bytes()
        if len(data) > max_bytes:
            raise ToolError("download exceeds byte limit: %s" % url, 1)
        return data, {"url": url, "status": 200, "cached": False}

    key = hashlib.sha256(url.encode("utf-8")).hexdigest()
    body_path = cache_dir / (key + ".body") if cache_dir else None
    meta_path = cache_dir / (key + ".json") if cache_dir else None
    cached_meta: Dict[str, Any] = {}
    if cache_dir:
        cache_dir.mkdir(parents=True, exist_ok=True)
        if meta_path and meta_path.exists():
            cached_meta = load_json(meta_path, {})
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json, application/octet-stream;q=0.8"}
    if cached_meta.get("etag"):
        headers["If-None-Match"] = str(cached_meta["etag"])
    if cached_meta.get("last_modified"):
        headers["If-Modified-Since"] = str(cached_meta["last_modified"])

    last_error: Optional[BaseException] = None
    for attempt in range(retries + 1):
        try:
            if limiter:
                limiter.wait(parsed.hostname or "")
            request = urllib.request.Request(url, headers=headers, method="GET")
            with urllib.request.urlopen(request, timeout=timeout) as response:
                content_length = response.headers.get("Content-Length")
                if content_length and int(content_length) > max_bytes:
                    raise ToolError("download exceeds byte limit: %s" % url, 1)
                data = response.read(max_bytes + 1)
                if len(data) > max_bytes:
                    raise ToolError("download exceeds byte limit: %s" % url, 1)
                meta = {
                    "url": response.geturl(),
                    "status": int(response.status),
                    "etag": response.headers.get("ETag"),
                    "last_modified": response.headers.get("Last-Modified"),
                    "cached": False,
                    "fetched_at": isoformat(utc_now()),
                }
                if body_path and meta_path:
                    atomic_write(body_path, data)
                    atomic_write_json(meta_path, meta)
                return data, meta
        except urllib.error.HTTPError as exc:
            if exc.code == 304 and body_path and body_path.exists():
                data = body_path.read_bytes()
                cached_meta.update({"status": 304, "cached": True})
                return data, cached_meta
            if exc.code not in (408, 425, 429, 500, 502, 503, 504):
                raise ToolError("HTTP %s for %s" % (exc.code, url), 1) from exc
            last_error = exc
            retry_after = exc.headers.get("Retry-After")
            delay = float(retry_after) if retry_after and retry_after.isdigit() else min(2 ** attempt, 16)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = exc
            delay = min(2 ** attempt, 16)
        if attempt < retries:
            time.sleep(delay)
    raise ToolError("failed to fetch %s after %d attempts: %s" % (url, retries + 1, last_error), 1)


def load_location(
    location: str,
    *,
    timeout: float = 30.0,
    retries: int = 3,
    cache_dir: Optional[pathlib.Path] = None,
    limiter: Optional[HostRateLimiter] = None,
) -> Tuple[Any, Dict[str, Any]]:
    if location.startswith(("https://", "file://")):
        content, metadata = fetch_url(
            location, timeout=timeout, retries=retries, cache_dir=cache_dir, limiter=limiter, max_bytes=512 * 1024 * 1024
        )
        return loads_document(content.decode("utf-8"), location), metadata
    path = pathlib.Path(location)
    return load_json(path), {"path": str(path), "sha256": sha256_file(path), "cached": False}


@contextlib.contextmanager
def locked_state(path: pathlib.Path) -> Iterator[MutableMapping[str, Any]]:
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = path.with_name(path.name + ".lock")
    with lock_path.open("a+b") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        state = load_json(path, {}) if path.exists() else {}
        if not isinstance(state, MutableMapping):
            raise ToolError("lease state must be an object")
        yield state
        atomic_write_json(path, state)
        fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def _canonical_tar_info(path: pathlib.Path, arcname: str) -> tarfile.TarInfo:
    info = tarfile.TarInfo(arcname)
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    info.mtime = 0
    if path.is_dir():
        info.type = tarfile.DIRTYPE
        info.mode = 0o755
        info.size = 0
    elif path.is_symlink():
        info.type = tarfile.SYMTYPE
        info.mode = 0o777
        info.size = 0
        info.linkname = os.readlink(path)
    elif path.is_file():
        info.type = tarfile.REGTYPE
        source_mode = stat.S_IMODE(path.stat().st_mode)
        info.mode = 0o755 if source_mode & 0o111 else 0o644
        info.size = path.stat().st_size
    else:
        raise ToolError("unsupported fixture entry: %s" % path)
    return info


def canonical_tar_gz(source_dir: pathlib.Path, destination: pathlib.Path, prefix: str) -> Dict[str, Any]:
    source_dir = source_dir.resolve()
    if not source_dir.is_dir():
        raise ToolError("fixture source is not a directory: %s" % source_dir)
    safe_prefix = slugify(prefix, 126)
    entries = [source_dir] + sorted(source_dir.rglob("*"), key=lambda item: item.relative_to(source_dir).as_posix())
    raw_tar = io.BytesIO()
    with tarfile.open(fileobj=raw_tar, mode="w", format=tarfile.PAX_FORMAT) as archive:
        for path in entries:
            relative = pathlib.PurePosixPath(".") if path == source_dir else pathlib.PurePosixPath(path.relative_to(source_dir).as_posix())
            arcname = safe_prefix if str(relative) == "." else "%s/%s" % (safe_prefix, relative)
            info = _canonical_tar_info(path, arcname)
            if info.isreg():
                with path.open("rb") as handle:
                    archive.addfile(info, handle)
            else:
                archive.addfile(info)
    destination.parent.mkdir(parents=True, exist_ok=True)
    compressed = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=compressed, mtime=0, compresslevel=9) as output:
        output.write(raw_tar.getvalue())
    atomic_write(destination, compressed.getvalue())
    return {
        "path": str(destination),
        "sha256": sha256_bytes(compressed.getvalue()),
        "size": len(compressed.getvalue()),
        "prefix": safe_prefix,
        "entries": len(entries),
    }


def tree_digest(root: pathlib.Path) -> str:
    root = root.resolve()
    if not root.is_dir():
        raise ToolError("tree path is not a directory: %s" % root)
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        if path.is_symlink():
            kind = b"L"
            content = os.readlink(path).encode("utf-8")
        elif path.is_dir():
            kind = b"D"
            content = b""
        elif path.is_file():
            kind = b"F"
            content = path.read_bytes()
        else:
            continue
        mode = b"x" if path.stat().st_mode & 0o111 else b"-"
        digest.update(kind + mode + b"\0" + relative + b"\0" + hashlib.sha256(content).digest())
    return digest.hexdigest()


def parse_source_assignment(value: str) -> Tuple[str, str]:
    if "=" not in value:
        raise ToolError("source input must use SOURCE=PATH_OR_URL: %s" % value)
    source, location = value.split("=", 1)
    source = source.strip().lower()
    if source not in {"arch", "aur", "opensuse", "fedora", "debian", "ubuntu"}:
        raise ToolError("unsupported discovery source: %s" % source)
    if not location.strip():
        raise ToolError("empty source location")
    if pathlib.PurePath(location).name.upper() == "PKGBUILD":
        raise ToolError("PKGBUILD input is forbidden; use trusted metadata such as AUR RPC or .SRCINFO")
    return source, location.strip()


def run_main(function: Any) -> None:
    try:
        code = function()
    except ToolError as exc:
        print("error: %s" % exc, file=os.sys.stderr)
        raise SystemExit(exc.exit_code)
    except KeyboardInterrupt:
        print("error: interrupted", file=os.sys.stderr)
        raise SystemExit(130)
    raise SystemExit(int(code or 0))
