# SPDX-License-Identifier: Apache-2.0
Name:           fastahack
Version:        1.0.0
Release:        1%{?dist}
Summary:        FASTA indexing and sequence extraction utility
License:        MIT AND GPL-2.0-or-later
URL:            https://github.com/ekg/fastahack
%global upstream_commit bb332654766c2177d6ec07941fe43facf8483b1d
Source0:        fastahack-1.0.0.tar.gz
Patch0:         0001-correct-subsequence-newline-offset.patch
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  libstdc++-devel
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  binutils
BuildRequires:  rpm
BuildRequires:  gzip
BuildRequires:  tar
BuildRequires:  patch
BuildRequires:  grep
BuildRequires:  gawk
BuildRequires:  sed
BuildRequires:  findutils
BuildRequires:  diffutils
Requires:       bash
Requires:       coreutils
Requires:       gawk
Requires:       grep
Requires:       diffutils
Requires:       rpm

%description
Fastahack indexes FASTA files and extracts sequences and indexed regions.
The executable includes the GPL-2.0-or-later libdisorder entropy implementation.

%prep
%autosetup -n fastahack-%{upstream_commit} -p1
mkdir -p contract
(cd tests && sha256sum *.fasta) > contract/SHA256SUMS
cat > contract/run-contract.sh <<'SH'
#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
test "$#" -le 2
root=${1:-/}
binary=${2:-${root%/}/usr/bin/fastahack}
self=$(cd -- "$(dirname -- "$0")" && pwd)
work=$(mktemp -d)
finish() {
    rc=$?
    if test "$rc" -eq 0; then rm -rf -- "$work"; else printf 'contract evidence retained: %s\n' "$work" >&2; fi
    exit "$rc"
}
trap finish EXIT
cd "$self"
sha256sum -c SHA256SUMS
for fixture in correct.fasta trailing_newlines.fasta crlf.fasta; do
    mkdir "$work/$fixture"
    cp "$fixture" "$work/$fixture/input.fasta"
    cd "$work/$fixture"
    "$binary" -i input.fasta > index.out 2> index.err
    test -s input.fasta.fai
    # Sequential parsing is an independent oracle, not indexed offset logic.
    awk 'BEGIN { OFS="\t" }
        /^>/ { if (name!="") print name,seq; name=substr($0,2); sub(/[ \t].*/,"",name); sub(/\r$/,"",name); seq=""; next }
        { gsub(/\r/,""); seq=seq $0 }
        END { if (name!="") print name,seq }' input.fasta > expected.dump
    test -s expected.dump
    "$binary" -d input.fasta > actual.dump
    cmp expected.dump actual.dump
    awk -F '\t' -v queries=regions -v answers=expected.regions '
        function emit(a,b) { print $1 ":" a "-" b > queries; print substr($2,a,b-a+1) > answers }
        { n=length($2); print $1 > queries; print $2 > answers;
          for (i=1;i<=n && i<=6;i++) emit(i,i);
          if (n>73) { emit(67,71); emit(68,68); emit(69,73) }
          emit(1,n); emit(n,n) }' expected.dump
    "$binary" -c input.fasta < regions > actual.regions
    cmp expected.regions actual.regions
    if test "$fixture" = crlf.fasta; then
        "$binary" -r chr:4 input.fasta > base4
        printf 'G\n' > expected.base4
        cmp expected.base4 base4
        "$binary" -r chr:2-5 input.fasta > range2-5
        printf 'AAGT\n' > expected.range2-5
        cmp expected.range2-5 range2-5
        "$binary" -e -r chr input.fasta > entropy
        awk 'BEGIN { ok=0 } /^[0-9]+([.][0-9]+)?$/ { if ($1>=1.918 && $1<=1.919) ok++ } END { exit !(NR==1 && ok==1) }' entropy
    fi
    printf 'PASS downstream retained valid fixture: %s\n' "$fixture"
    cd "$self"
done
for fixture in embedded_newline.fasta mismatched_lines.fasta; do
    mkdir "$work/$fixture"
    cp "$fixture" "$work/$fixture/input.fasta"
    cd "$work/$fixture"
    if "$binary" -i input.fasta > index.out 2> index.err; then
        printf 'invalid fixture unexpectedly accepted: %s\n' "$fixture" >&2
        exit 1
    fi
    case "$fixture" in
        embedded_newline.fasta) grep -F 'ERROR: embedded newline' index.err ;;
        mismatched_lines.fasta) grep -F 'ERROR: mismatched line lengths' index.err ;;
    esac
    test ! -e input.fasta.fai
    printf 'PASS downstream retained invalid fixture: %s\n' "$fixture"
    cd "$self"
done
"$binary" -h > "$work/help.out" 2> "$work/help.err"
grep -i usage "$work/help.out" "$work/help.err"
if "$binary" > "$work/noarg.out" 2> "$work/noarg.err"; then exit 1; fi
if "$binary" -i "$work/absent.fasta" > "$work/missing.out" 2> "$work/missing.err"; then exit 1; fi
cd "$work/correct.fasta"
if "$binary" -r absent input.fasta > "$work/unknown.out" 2> "$work/unknown.err"; then exit 1; fi
grep -F 'unable to find FASTA index entry' "$work/unknown.err"
printf 'PASS downstream contract: retained-fixtures=5 original-registered-tests=0 CLI-negative=3 entropy=verified\n'
SH

%build
export CXX=g++
# Environment assignment preserves upstream's appended large-file definition.
export CXXFLAGS="%{optflags} -g -UNDEBUG %{?build_ldflags}"
%make_build

%install
%make_install PREFIX=%{_prefix}
install -d %{buildroot}%{_datadir}/fastahack/tests
install -m 0644 tests/*.fasta contract/SHA256SUMS %{buildroot}%{_datadir}/fastahack/tests/
install -m 0755 contract/run-contract.sh %{buildroot}%{_datadir}/fastahack/tests/

%check
# Upstream registers no check target; all five original fixtures are unchanged.
bash %{buildroot}%{_datadir}/fastahack/tests/run-contract.sh %{buildroot} "$PWD/fastahack"
bash %{buildroot}%{_datadir}/fastahack/tests/run-contract.sh %{buildroot}

%files
%license LICENSE libdisorder.LICENSE
%doc README disorder.c disorder.h
%{_bindir}/fastahack
%{_datadir}/fastahack/

%changelog
* Fri Oct 16 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Package the default CLI and retain all upstream FASTA fixtures.
- Correct indexed LF/CRLF subsequence newline offsets without disabling features.
