#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail

rootfs=${1:-}
repo_file=${2:-}
repo_url=https://repo.openeuler.org/openEuler-24.03-LTS-SP3/everything/riscv64/rva23/riscv64/

die() {
  printf 'bootstrap-rootfs: %s\n' "$*" >&2
  exit 2
}

download_verified_resumable() {
  local url=$1
  local expected_sha256=$2
  local output=$3
  local partial=${output}.partial
  local attempt

  [[ $expected_sha256 =~ ^[0-9a-f]{64}$ ]] || die "invalid expected download checksum"
  rm -f -- "$output" "$partial"
  for attempt in 1 2 3 4 5; do
    if curl --fail --location --proto '=https' --tlsv1.2 \
      --continue-at - --connect-timeout 20 --max-time 300 \
      "$url" -o "$partial"; then
      printf '%s  %s\n' "$expected_sha256" "$partial" \
        | sha256sum --check --strict \
        || die "completed repository download failed its authenticated checksum"
      mv -f -- "$partial" "$output"
      return 0
    fi
    if (( attempt < 5 )); then
      printf 'bootstrap-rootfs: resumable download attempt %d/5 failed; retrying in 2 seconds\n' \
        "$attempt" >&2
      sleep 2
    fi
  done
  die "authenticated repository download failed after five resumable attempts"
}

[[ $rootfs == /rootfs ]] || die "the build root must be exactly /rootfs"
[[ -f $repo_file ]] || die "repository file is missing: $repo_file"
grep -Fqx "baseurl=${repo_url}" "$repo_file" || die "repository URL differs from the approved RVA23 repository"
grep -Fqx 'gpgcheck=1' "$repo_file" || die "RPM signature verification must remain enabled"

# The build stage is disposable. Recreate the target so stale RPM databases or
# caches can never influence an evidence-producing image build.
rm -rf -- "$rootfs"
install -d -m 0755 "$rootfs" /evidence

curl --fail --location --proto '=https' --tlsv1.2 \
  --retry 4 --retry-delay 2 --connect-timeout 20 --max-time 180 \
  "${repo_url}repodata/repomd.xml" -o /evidence/repomd.before.xml
sha256sum /evidence/repomd.before.xml | awk '{print $1}' > /evidence/repomd.sha256

# Bootstrap the signing key without disabling RPM verification. The key RPM is
# selected from primary.sqlite, whose compressed digest is authenticated by the
# HTTPS-fetched repomd.xml. The key RPM itself is then checked against pkgId.
read -r primary_href primary_checksum < <(python3 - /evidence/repomd.before.xml <<'PY'
import sys
import xml.etree.ElementTree as ET

root = ET.parse(sys.argv[1]).getroot()
ns = {"repo": "http://linux.duke.edu/metadata/repo"}
for data in root.findall("repo:data", ns):
    if data.attrib.get("type") == "primary_db":
        checksum = data.find("repo:checksum", ns)
        location = data.find("repo:location", ns)
        if checksum is None or checksum.attrib.get("type") != "sha256" or location is None:
            raise SystemExit("primary_db does not carry a sha256 checksum and location")
        print(location.attrib["href"], checksum.text)
        break
else:
    raise SystemExit("primary_db is missing from repomd.xml")
PY
)
[[ $primary_href == repodata/* && $primary_href != *..* ]] || die "unsafe primary_db path"
[[ $primary_checksum =~ ^[0-9a-f]{64}$ ]] || die "invalid primary_db checksum"
download_verified_resumable \
  "${repo_url}${primary_href}" "$primary_checksum" /evidence/primary.sqlite.bz2
printf '%s  %s\n' "$primary_checksum" /evidence/primary.sqlite.bz2 | sha256sum --check --strict
bzip2 -dc /evidence/primary.sqlite.bz2 > /evidence/primary.sqlite

read -r key_href key_checksum < <(python3 - /evidence/primary.sqlite <<'PY'
import sqlite3
import sys

connection = sqlite3.connect(f"file:{sys.argv[1]}?mode=ro", uri=True)
row = connection.execute(
    "SELECT location_href, pkgId FROM packages WHERE name = ? ORDER BY pkgKey DESC LIMIT 1",
    ("openEuler-gpg-keys",),
).fetchone()
if not row:
    raise SystemExit("openEuler-gpg-keys is absent from primary metadata")
print(row[0], row[1])
PY
)
[[ $key_href == Packages/* && $key_href != *..* ]] || die "unsafe signing-key RPM path"
[[ $key_checksum =~ ^[0-9a-f]{64}$ ]] || die "invalid signing-key RPM checksum"
download_verified_resumable \
  "${repo_url}${key_href}" "$key_checksum" /evidence/openEuler-gpg-keys.rpm
printf '%s  %s\n' "$key_checksum" /evidence/openEuler-gpg-keys.rpm | sha256sum --check --strict
install -d -m 0755 /bootstrap/key-rpm /bootstrap/repos
(cd /bootstrap/key-rpm && rpm2cpio /evidence/openEuler-gpg-keys.rpm | cpio -idm --quiet)
key_file=$(find /bootstrap/key-rpm/etc/pki/rpm-gpg -type f -name 'RPM-GPG-KEY-openEuler*' -print -quit)
[[ -n $key_file ]] || die "signing-key RPM did not contain the expected openEuler key"
sed "s|^gpgkey=.*|gpgkey=file://${key_file}|" "$repo_file" > /bootstrap/repos/openeuler-rva23.repo
printf '%s\n' "$primary_href" > /evidence/primary-db.href
printf '%s\n' "$primary_checksum" > /evidence/primary-db.sha256
printf '%s\n' "$key_href" > /evidence/signing-key-rpm.href
printf '%s\n' "$key_checksum" > /evidence/signing-key-rpm.sha256

packages=(
  bash bzip2 ca-certificates coreutils cpio curl diffutils dnf file findutils
  gawk gcc gcc-c++ git glibc glibc-langpack-en grep gzip make patch
  python3 rpm rpm-build sed shadow tar unzip util-linux which xz
)

# The official endpoint is bandwidth-constrained and has repeatedly reset
# concurrent HTTP/2 streams. Serialize payloads and retain completed downloads
# across two bounded transaction attempts; the disposable cache is removed below.
/bootstrap/run-dnf-transaction \
  --evidence /evidence/bootstrap-dnf-transaction.json \
  --budget-seconds 7300 \
  --attempt-timeouts-seconds 4200,3000 \
  --retry-delay-seconds 5 \
  --kill-after-seconds 30 \
  -- dnf -y \
    --installroot "$rootfs" \
    --forcearch riscv64 \
    --setopt reposdir=/bootstrap/repos \
    --setopt install_weak_deps=False \
    --setopt keepcache=True \
    --disablerepo='*' \
    --enablerepo=openeuler-rva23 \
    install "${packages[@]}"

# Record the database path actually used by the bootstrap RPM implementation.
# The target stage never copies this backend-specific database. It imports the
# verified portable header stream below into a database generated by target
# RPM, at the path evaluated by target RPM itself.
bootstrap_rpmdb=$(rpm --root "$rootfs" --eval '%{_dbpath}')
[[ $bootstrap_rpmdb =~ ^/[A-Za-z0-9._/-]+$ \
   && $bootstrap_rpmdb != / \
   && $bootstrap_rpmdb != *//* ]] \
  || die "bootstrap RPM returned an unsafe database path"
IFS=/ read -r -a bootstrap_rpmdb_components <<<"$bootstrap_rpmdb"
for component in "${bootstrap_rpmdb_components[@]}"; do
  [[ $component != . && $component != .. ]] \
    || die "bootstrap RPM database path contains a traversal component"
done
bootstrap_rpmdb_host=${rootfs}${bootstrap_rpmdb}
[[ -d $bootstrap_rpmdb_host && ! -L $bootstrap_rpmdb_host ]] \
  || die "bootstrap RPM database path does not contain a regular directory"
[[ -n $(find "$bootstrap_rpmdb_host" -mindepth 1 -maxdepth 1 -print -quit) ]] \
  || die "bootstrap RPM database directory is empty"
printf '%s\n' "$bootstrap_rpmdb" > /evidence/bootstrap-rpmdb.path

curl --fail --location --proto '=https' --tlsv1.2 \
  --retry 4 --retry-delay 2 --connect-timeout 20 --max-time 180 \
  "${repo_url}repodata/repomd.xml" -o /evidence/repomd.after.xml
cmp -s /evidence/repomd.before.xml /evidence/repomd.after.xml \
  || die "repository metadata changed during rootfs construction; retry from a clean run"

/bootstrap/rpm-manifest.sh "$rootfs" > /evidence/rpm-manifest.tsv
[[ -s /evidence/rpm-manifest.tsv ]] || die "bootstrap RPM manifest is empty"
# RPM records imported signing keys as the pseudo-package gpg-pubkey, whose
# architecture is rendered as "(none)". Allow only that exact pseudo-record;
# every installed payload package must still be riscv64 or noarch.
awk -F '\t' '($3 != "riscv64" && $3 != "noarch") && !($1 == "gpg-pubkey" && $3 == "(none)") {print; bad=1} END {exit bad}' \
  /evidence/rpm-manifest.tsv || die "rootfs contains an RPM for an unexpected architecture"
sha256sum /evidence/rpm-manifest.tsv | awk '{print $1}' > /evidence/rpm-manifest.sha256

# RPM's documented header-list transport is independent of the source
# database backend and is explicitly intended for another host or database
# type. Verify both the source database and a clean import round trip before
# embedding the stream for the target RPM implementation.
rpmdb --root "$rootfs" --verifydb
rpmdb --root "$rootfs" --exportdb > /evidence/rpmdb-header-list.bin
[[ -s /evidence/rpmdb-header-list.bin ]] || die "portable RPM database export is empty"
sha256sum /evidence/rpmdb-header-list.bin | awk '{print $1}' \
  > /evidence/rpmdb-header-list.sha256
roundtrip_db=/bootstrap/rpmdb-header-list-roundtrip
[[ ! -e $roundtrip_db ]] || die "portable RPM database round-trip path already exists"
install -d -m 0700 "$roundtrip_db"
rpmdb --dbpath "$roundtrip_db" --importdb < /evidence/rpmdb-header-list.bin
rpmdb --dbpath "$roundtrip_db" --verifydb
/bootstrap/rpm-manifest.sh --dbpath "$roundtrip_db" \
  > /evidence/rpm-manifest-roundtrip.tsv
cmp -s /evidence/rpm-manifest.tsv /evidence/rpm-manifest-roundtrip.tsv \
  || die "portable RPM database export does not reproduce the installed manifest"
rpmdb --dbpath "$roundtrip_db" --exportdb \
  > /evidence/rpmdb-header-list-roundtrip.bin
cmp -s /evidence/rpmdb-header-list.bin /evidence/rpmdb-header-list-roundtrip.bin \
  || die "portable RPM database header stream is not an exact round trip"

install -d -m 0755 "$rootfs/usr/share/openeuler-riscv-ci" "$rootfs/etc/yum.repos.d"
install -m 0644 /evidence/bootstrap-dnf-transaction.json \
  "$rootfs/usr/share/openeuler-riscv-ci/bootstrap-dnf-transaction.json"
root_key=$(find "$rootfs/etc/pki/rpm-gpg" -type f -name 'RPM-GPG-KEY-openEuler*' -print -quit)
[[ -n $root_key ]] || die "installed rootfs does not contain the openEuler signing key"
root_key_path=${root_key#"$rootfs"}
sed "s|^gpgkey=.*|gpgkey=file://${root_key_path}|" "$repo_file" \
  > "$rootfs/etc/yum.repos.d/openeuler-rva23.repo"
install -m 0644 /evidence/repomd.before.xml "$rootfs/usr/share/openeuler-riscv-ci/repomd.xml"
install -m 0644 /evidence/repomd.sha256 "$rootfs/usr/share/openeuler-riscv-ci/repomd.sha256"
install -m 0644 /evidence/rpm-manifest.tsv "$rootfs/usr/share/openeuler-riscv-ci/rpm-manifest.tsv"
install -m 0644 /evidence/rpm-manifest.sha256 "$rootfs/usr/share/openeuler-riscv-ci/rpm-manifest.sha256"
install -m 0644 /evidence/bootstrap-rpmdb.path "$rootfs/usr/share/openeuler-riscv-ci/bootstrap-rpmdb.path"
install -m 0644 /evidence/rpmdb-header-list.bin "$rootfs/usr/share/openeuler-riscv-ci/rpmdb-header-list.bin"
install -m 0644 /evidence/rpmdb-header-list.sha256 "$rootfs/usr/share/openeuler-riscv-ci/rpmdb-header-list.sha256"
install -m 0644 /evidence/primary-db.href "$rootfs/usr/share/openeuler-riscv-ci/primary-db.href"
install -m 0644 /evidence/primary-db.sha256 "$rootfs/usr/share/openeuler-riscv-ci/primary-db.sha256"
install -m 0644 /evidence/signing-key-rpm.href "$rootfs/usr/share/openeuler-riscv-ci/signing-key-rpm.href"
install -m 0644 /evidence/signing-key-rpm.sha256 "$rootfs/usr/share/openeuler-riscv-ci/signing-key-rpm.sha256"

rm -rf -- "$rootfs/var/cache/dnf" "$rootfs/var/log/dnf"* "$rootfs/var/log/hawkey.log"
find "$rootfs/var/log" -type f -exec truncate -s 0 {} +

# Do not evaluate %{_arch} with the bootstrap-stage RPM binary: that process
# runs on BUILDPLATFORM and reports the host architecture even with --root.
# The target-platform RUN in Containerfile.riscv64 executes verify-target under
# QEMU and enforces the riscv64 RPM macro after this manifest audit.
grep -Eqi '24\.03.*LTS.*SP3|24\.03-LTS-SP3' "$rootfs/etc/openEuler-release" \
  || die "rootfs release is not openEuler 24.03 LTS SP3"
