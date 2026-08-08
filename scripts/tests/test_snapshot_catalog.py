# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import gzip
import hashlib
import io
import json
import pathlib
import tarfile
import tempfile
import unittest
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

from helpers import run_tool, write_json


AS_OF = "2026-08-08T00:00:00Z"


def fixture_url(relative: str) -> str:
    return "fixture:///" + relative.lstrip("/")


def write_bytes(root: pathlib.Path, relative: str, data: bytes) -> pathlib.Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def pacman_database(packages: Sequence[Mapping[str, Any]]) -> bytes:
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w") as archive:
        for package in packages:
            fields = {
                "NAME": [package["name"]],
                "BASE": [package.get("base", package["name"])],
                "VERSION": [package["version"]],
                "DESC": [package.get("description", "fixture package")],
                "URL": [package["url"]],
                "LICENSE": list(package.get("license", ["MIT"])),
                "ARCH": ["x86_64"],
                "BUILDDATE": [str(package.get("builddate", 1786000000))],
                "FILENAME": [package["name"] + "-fixture.pkg.tar.zst"],
                "SHA256SUM": ["a" * 64],
            }
            text = "".join(
                "%%%s%%\n%s\n\n" % (key, "\n".join(str(item) for item in values))
                for key, values in fields.items()
            ).encode("utf-8")
            info = tarfile.TarInfo("%s-%s/desc" % (package["name"], package["version"]))
            info.size = len(text)
            info.mode = 0o644
            archive.addfile(info, io.BytesIO(text))
    return gzip.compress(raw.getvalue(), mtime=0)


def rpm_primary(package_name: str, version: str = "1.0", release: str = "1") -> bytes:
    text = """<?xml version="1.0" encoding="UTF-8"?>
<metadata xmlns="http://linux.duke.edu/metadata/common"
          xmlns:rpm="http://linux.duke.edu/metadata/rpm" packages="1">
  <package type="rpm">
    <name>{name}</name><arch>src</arch>
    <version epoch="0" ver="{version}" rel="{release}"/>
    <checksum type="sha256" pkgid="YES">{checksum}</checksum>
    <summary>{name} source package</summary><description>fixture</description>
    <url>https://example.org/{name}</url>
    <time file="1786000000" build="1786000000"/>
    <location href="src/{name}-{version}-{release}.src.rpm"/>
    <format><rpm:license>Apache-2.0</rpm:license><rpm:packager>Fixture Builder</rpm:packager></format>
  </package>
</metadata>
""".format(name=package_name, version=version, release=release, checksum="b" * 64)
    return gzip.compress(text.encode("utf-8"), mtime=0)


def write_rpm_repository(
    root: pathlib.Path,
    relative: str,
    package_name: str,
    checksum_type: str = "sha256",
) -> str:
    primary = rpm_primary(package_name)
    write_bytes(root, relative + "/repodata/primary.xml.gz", primary)
    repomd = """<?xml version="1.0" encoding="UTF-8"?>
<repomd xmlns="http://linux.duke.edu/metadata/repo">
  <revision>20260808</revision>
  <data type="primary">
    <checksum type="{checksum_type}">{digest}</checksum>
    <location href="repodata/primary.xml.gz"/>
    <timestamp>1786147200</timestamp>
  </data>
</repomd>
""".format(
        checksum_type=checksum_type,
        digest=hashlib.new(checksum_type, primary).hexdigest(),
    ).encode("utf-8")
    write_bytes(root, relative + "/repodata/repomd.xml", repomd)
    return fixture_url(relative + "/repodata/repomd.xml")


def source_paragraph(package: str) -> str:
    upstream = (package + "-1.0.orig.tar.gz").encode("utf-8")
    digest = hashlib.sha256(upstream).hexdigest()
    return """Package: {package}
Binary: {package}
Version: 1.0-1
Maintainer: Fixture Maintainer <fixture@example.org>
Homepage: https://example.org/{package}
Directory: pool/main/{initial}/{package}
Checksums-Sha256:
 {digest} {size} {package}-1.0.orig.tar.gz

""".format(package=package, initial=package[0], digest=digest, size=len(upstream))


def write_deb_release(
    root: pathlib.Path,
    relative: str,
    *,
    suite: str,
    codename: str,
    version: str,
    components: Sequence[str],
    prefix: str,
) -> str:
    checksums: List[Tuple[str, int, str]] = []
    for component in components:
        paragraph = source_paragraph("%s-%s" % (prefix, component.replace("-", "")))
        content = gzip.compress(paragraph.encode("utf-8"), mtime=0)
        path = "%s/source/Sources.gz" % component
        write_bytes(root, relative + "/" + path, content)
        checksums.append((hashlib.sha256(content).hexdigest(), len(content), path))
    release = """Origin: Fixture
Suite: {suite}
Version: {version}
Codename: {codename}
Date: Fri, 08 Aug 2026 00:00:00 UTC
Components: {components}
SHA256:
{checksums}
""".format(
        suite=suite,
        version=version,
        codename=codename,
        components=" ".join(components),
        checksums="\n".join(" %s %d %s" % item for item in checksums),
    ).encode("utf-8")
    write_bytes(root, relative + "/Release", release)
    return fixture_url(relative + "/Release")


def base_config(sources: Mapping[str, Any]) -> Dict[str, Any]:
    return {"schema_version": "1.0", "sources": dict(sources)}


class SnapshotCatalogTests(unittest.TestCase):
    def test_arch_and_aur_snapshots_are_safe_normalized_and_consumable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            fixtures = root / "fixtures"
            core = pacman_database(
                [{"name": "alpha", "version": "1.2.0-1", "url": "https://example.org/alpha"}]
            )
            extra = pacman_database(
                [{"name": "beta", "version": "2.0-1", "url": "https://example.org/beta"}]
            )
            write_bytes(fixtures, "arch/core.db", core)
            write_bytes(fixtures, "arch/extra.db", extra)
            sentinel = root / "aur-content-was-executed"
            aur_document = [
                {
                    "Name": "alpha-git",
                    "PackageBase": "alpha-git",
                    "Version": "r20.abc",
                    "Description": "untrusted $(touch %s)" % sentinel,
                    "URL": "https://example.org/alpha",
                    "License": ["MIT"],
                    "Maintainer": "fixture",
                    "LastModified": 1786000000,
                    "OutOfDate": None,
                    "URLPath": "/cgit/aur.git/snapshot/alpha-git.tar.gz",
                },
                {
                    "Name": "gamma",
                    "PackageBase": "gamma",
                    "Version": "3.1",
                    "URL": "https://example.org/gamma",
                    "License": ["BSD-2-Clause"],
                    "LastModified": 1786000000,
                },
            ]
            write_bytes(
                fixtures,
                "aur/packages-meta-ext-v1.json.gz",
                gzip.compress(json.dumps(aur_document).encode("utf-8"), mtime=0),
            )
            config = root / "sources.yaml"
            write_json(
                config,
                base_config(
                    {
                        "arch": {
                            "enabled": True,
                            "repositories": ["core", "extra"],
                            "metadata_urls": [
                                fixture_url("arch/core.db"),
                                fixture_url("arch/extra.db"),
                            ],
                        },
                        "aur": {
                            "enabled": True,
                            "metadata_urls": [fixture_url("aur/packages-meta-ext-v1.json.gz")],
                        },
                    }
                ),
            )
            output = root / "snapshots"
            summary = root / "summary.json"
            run_tool(
                "snapshot-catalog",
                [
                    "--config", str(config),
                    "--source", "arch",
                    "--source", "aur",
                    "--output-dir", str(output),
                    "--summary", str(summary),
                    "--cache-dir", str(root / "cache"),
                    "--fixture-root", str(fixtures),
                    "--as-of", AS_OF,
                    "--limit", "1",
                ],
                root,
            )
            self.assertFalse(sentinel.exists(), "AUR metadata content must never execute")
            arch = json.loads((output / "arch.json").read_text(encoding="utf-8"))
            aur = json.loads((output / "aur.json").read_text(encoding="utf-8"))
            self.assertEqual(arch["snapshot"]["components"], ["core", "extra"])
            self.assertEqual(arch["summary"]["package_count_before_limit"], 2)
            self.assertEqual(arch["packages"][0]["name"], "alpha")
            self.assertIsNone(arch["packages"][0]["source_url"])
            self.assertEqual(aur["summary"]["package_count_before_limit"], 2)
            self.assertFalse(aur["snapshot"]["external_packaging_executed"])
            self.assertRegex(aur["snapshot"]["metadata_sha256"], r"^[0-9a-f]{64}$")
            result = json.loads(summary.read_text(encoding="utf-8"))
            self.assertEqual(result["status"], "complete")
            self.assertEqual(result["total_packages"], 2)
            self.assertEqual(set(result["sources"]), {"arch", "aur"})

            discovery = root / "discovery.json"
            run_tool(
                "discover-packages",
                [
                    "--input", "arch=%s" % (output / "arch.json"),
                    "--input", "aur=%s" % (output / "aur.json"),
                    "--output", str(discovery),
                    "--as-of", AS_OF,
                ],
                root,
            )
            self.assertTrue(discovery.is_file())

    def test_supplemental_sources_resolve_stable_releases_and_all_components(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            fixtures = root / "fixtures"
            opensuse_oss = write_rpm_repository(
                fixtures, "opensuse/repo/oss", "suse-oss", checksum_type="sha512"
            )
            opensuse_nonoss = write_rpm_repository(
                fixtures, "opensuse/repo/non-oss", "suse-nonoss", checksum_type="sha512"
            )

            write_bytes(
                fixtures,
                "fedora/releases/index.html",
                b'<a href="43/">43</a><a href="44/">44</a><a href="rawhide/">Rawhide</a>'
                b'<a href="45_Branched/">Branched</a>',
            )
            write_rpm_repository(fixtures, "fedora/releases/44/Everything/source/tree", "fedora-source")

            debian_release = write_deb_release(
                fixtures,
                "debian/dists/stable",
                suite="stable",
                codename="trixie",
                version="13.6",
                components=("main", "contrib", "non-free", "non-free-firmware"),
                prefix="debian",
            )

            ubuntu_release = write_deb_release(
                fixtures,
                "ubuntu/dists/resolute",
                suite="resolute",
                codename="resolute",
                version="26.04.1",
                components=("main", "restricted", "universe", "multiverse"),
                prefix="ubuntu",
            )
            ubuntu_updates_release = write_deb_release(
                fixtures,
                "ubuntu/dists/resolute-updates",
                suite="resolute-updates",
                codename="resolute-updates",
                version="26.04.1",
                components=("main", "restricted", "universe", "multiverse"),
                prefix="ubuntu-update",
            )
            meta_release = """Dist: obsolete
Name: Obsolete
Version: 24.10
Date: Thu, 10 Oct 2024 00:00:00 UTC
Supported: 0
Release-File: {obsolete}

Dist: future
Name: Future Development Preview
Version: 26.10
Date: Thu, 08 Oct 2026 00:00:00 UTC
Supported: 1
Release-File: {future}

Dist: resolute
Name: Resolute Release
Version: 26.04.1 LTS
Date: Thu, 23 Apr 2026 00:00:00 UTC
Supported: 1
Release-File: {release}

""".format(
                obsolete=fixture_url("ubuntu/dists/obsolete/Release"),
                future=fixture_url("ubuntu/dists/future/Release"),
                release=ubuntu_updates_release,
            ).encode("utf-8")
            write_bytes(fixtures, "ubuntu/meta-release", meta_release)
            write_bytes(fixtures, "ubuntu/meta-release-lts", meta_release)

            config = root / "sources.yaml"
            write_json(
                config,
                base_config(
                    {
                        "opensuse": {
                            "enabled": True,
                            "components": ["oss", "non-oss"],
                            "metadata_urls": [
                                {"url": opensuse_oss, "component": "oss"},
                                {"url": opensuse_nonoss, "component": "non-oss"},
                            ],
                        },
                        "fedora": {
                            "enabled": True,
                            "components": ["Everything-source"],
                            "metadata_urls": [fixture_url("fedora/releases/")],
                        },
                        "debian": {
                            "enabled": True,
                            "components": ["main", "contrib", "non-free", "non-free-firmware"],
                            "metadata_urls": [debian_release],
                        },
                        "ubuntu": {
                            "enabled": True,
                            "components": ["main", "restricted", "universe", "multiverse"],
                            "metadata_urls": [
                                fixture_url("ubuntu/meta-release"),
                                fixture_url("ubuntu/meta-release-lts"),
                            ],
                        },
                    }
                ),
            )
            output = root / "snapshots"
            run_tool(
                "snapshot-catalog",
                [
                    "--config", str(config),
                    "--output-dir", str(output),
                    "--fixture-root", str(fixtures),
                    "--as-of", AS_OF,
                    "--requests-per-second", "1000",
                ],
                root,
            )
            opensuse = json.loads((output / "opensuse.json").read_text(encoding="utf-8"))
            fedora = json.loads((output / "fedora.json").read_text(encoding="utf-8"))
            debian = json.loads((output / "debian.json").read_text(encoding="utf-8"))
            ubuntu = json.loads((output / "ubuntu.json").read_text(encoding="utf-8"))
            self.assertEqual(opensuse["snapshot"]["resolved_release"], "Tumbleweed")
            self.assertEqual({item["repository"] for item in opensuse["packages"]}, {"oss", "non-oss"})
            self.assertEqual(fedora["snapshot"]["resolved_release"], "44")
            self.assertFalse(fedora["snapshot"]["rawhide_or_branched_selected"])
            self.assertEqual(debian["snapshot"]["codename"], "trixie")
            self.assertEqual(debian["snapshot"]["resolved_release"], "13.6")
            self.assertEqual(len(debian["packages"]), 4)
            self.assertEqual(ubuntu["snapshot"]["codename"], "resolute")
            self.assertEqual(ubuntu["snapshot"]["resolved_release"], "26.04.1 LTS")
            self.assertTrue(ubuntu["snapshot"]["standard_support"])
            self.assertEqual(len(ubuntu["packages"]), 4)
            normalized_ubuntu_release = ubuntu_release.replace("fixture:///", "fixture:/")
            self.assertEqual(ubuntu["snapshot"]["base_release_file"], normalized_ubuntu_release)
            self.assertEqual(ubuntu["snapshot"]["meta_release_file"], ubuntu_updates_release)
            self.assertIn(normalized_ubuntu_release, ubuntu["snapshot"]["source_urls"])
            self.assertNotIn(ubuntu_updates_release, ubuntu["snapshot"]["source_urls"])
            for document in (opensuse, fedora, debian, ubuntu):
                self.assertEqual(document["snapshot"]["snapshot_at"], AS_OF)
                self.assertTrue(document["snapshot"]["source_urls"])
                for item in document["snapshot"]["metadata"]:
                    self.assertRegex(item["sha256"], r"^[0-9a-f]{64}$")

    def test_unsupported_metadata_fails_closed_without_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            fixtures = root / "fixtures"
            write_bytes(fixtures, "opensuse/repo/oss/repodata/primary.xml.zck", b"not-zchunk")
            repomd = """<repomd xmlns="http://linux.duke.edu/metadata/repo">
  <data type="primary"><checksum type="sha256">{digest}</checksum>
  <location href="repodata/primary.xml.zck"/></data>
</repomd>""".format(digest=hashlib.sha256(b"not-zchunk").hexdigest()).encode("utf-8")
            write_bytes(fixtures, "opensuse/repo/oss/repodata/repomd.xml", repomd)
            write_rpm_repository(fixtures, "opensuse/repo/non-oss", "nonoss")
            config = root / "sources.yaml"
            write_json(
                config,
                base_config(
                    {
                        "opensuse": {
                            "enabled": True,
                            "components": ["oss", "non-oss"],
                            "metadata_urls": [
                                {"url": fixture_url("opensuse/repo/oss/repodata/repomd.xml"), "component": "oss"},
                                {
                                    "url": fixture_url(
                                        "opensuse/repo/non-oss/repodata/repomd.xml"
                                    ),
                                    "component": "non-oss",
                                },
                            ],
                        }
                    }
                ),
            )
            output = root / "snapshots"
            completed = run_tool(
                "snapshot-catalog",
                [
                    "--config", str(config),
                    "--output-dir", str(output),
                    "--fixture-root", str(fixtures),
                    "--as-of", AS_OF,
                ],
                root,
                expected=1,
            )
            self.assertIn("unsupported metadata compression/format", completed.stderr)
            self.assertFalse((output / "opensuse.json").exists())
            self.assertFalse((output / "summary.json").exists())

    def test_aur_pkgbuild_endpoint_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            fixtures = root / "fixtures"
            write_bytes(fixtures, "aur/PKGBUILD", b"touch should-never-run\n")
            config = root / "sources.yaml"
            write_json(
                config,
                base_config(
                    {
                        "aur": {
                            "enabled": True,
                            "metadata_urls": [fixture_url("aur/PKGBUILD")],
                        }
                    }
                ),
            )
            completed = run_tool(
                "snapshot-catalog",
                [
                    "--config", str(config),
                    "--output-dir", str(root / "snapshots"),
                    "--fixture-root", str(fixtures),
                    "--as-of", AS_OF,
                ],
                root,
                expected=2,
            )
            self.assertIn("PKGBUILD input is forbidden", completed.stderr)


if __name__ == "__main__":
    unittest.main()
