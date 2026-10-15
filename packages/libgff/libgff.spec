# SPDX-License-Identifier: Apache-2.0
Name:           libgff
Version:        2.0.1
Release:        1%{?dist}
Summary:        C++ GFF and GTF annotation parser library
License:        BSL-1.0
URL:            https://github.com/COMBINE-lab/libgff
Source0:        https://codeload.github.com/COMBINE-lab/libgff/tar.gz/112721772d5c118f8ddf059395e88057b00067e6#/libgff-2.0.1.tar.gz
Patch0:         0001-use-configured-library-install-directory.patch
BuildRequires:  gcc-c++ cmake make glibc-devel bash coreutils rpm gzip tar gawk

%description
GFF/GTF parsing code derived from GFFRead and GCLib, exposed as a C++ library.
The original default static library and TestGFFParse executable are built.

%package devel
Summary:        Original headers, static library and CMake configuration
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc-c++ cmake make glibc-devel bash coreutils rpm gawk

%description devel
Original flat public headers, static archive and CMake configuration. Original
TestGFFParse source and downstream fixtures verify installed consumers.

%prep
%autosetup -n libgff-112721772d5c118f8ddf059395e88057b00067e6 -p1
cat > fixture.gtf <<'GTF'
chr1	downstream	exon	101	150	.	+	.	gene_id "gene1"; transcript_id "tx1";
chr1	downstream	exon	201	250	.	+	.	gene_id "gene1"; transcript_id "tx1";
chr2	downstream	exon	301	350	.	-	.	gene_id "gene2"; transcript_id "tx2";
GTF
: > empty.gtf
cat > check-parser.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
parser=$1
outdir=$2
mkdir -p "$outdir"
"$parser" fixture.gtf > "$outdir/parsed" 2> "$outdir/count"
test "$(wc -l < "$outdir/parsed")" -eq 2
test "$(awk -F '\t' '$1=="tx1" && $2=="gene1" {n++} END {print n+0}' "$outdir/parsed")" -eq 1
test "$(awk -F '\t' '$1=="tx2" && $2=="gene2" {n++} END {print n+0}' "$outdir/parsed")" -eq 1
test "$(cat "$outdir/count")" = 'had count of 2'
"$parser" empty.gtf > "$outdir/empty" 2> "$outdir/empty-count"
test ! -s "$outdir/empty"
test "$(cat "$outdir/empty-count")" = 'had count of 0'
set +e
"$parser" > "$outdir/usage" 2> "$outdir/usage-err"
code=$?
set -e
test "$code" -eq 1
test "$(cat "$outdir/usage-err")" = 'Usage: TestGFFParse input'
echo 'PASS downstream-fixtures checks=8 skips=0 original-parser-source=unchanged'
SH

%build
cmake -S . -B build -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DCMAKE_CXX_FLAGS_RELWITHDEBINFO="" \
    -DCMAKE_CXX_FLAGS="%{optflags} -UNDEBUG"
cmake --build build --parallel %{_smp_build_ncpus}

%install
DESTDIR=%{buildroot} cmake --install build
install -d %{buildroot}%{_datadir}/libgff/tests
install -m 0644 src/TestGFFParse.cpp fixture.gtf empty.gtf check-parser.sh \
    %{buildroot}%{_datadir}/libgff/tests/
(cd src && sha256sum TestGFFParse.cpp) > %{buildroot}%{_datadir}/libgff/tests/SHA256SUMS

%check
# Upstream registers no CTest tests. Preserve and execute its original default
# TestGFFParse program with explicitly downstream (not upstream suite) fixtures.
bash check-parser.sh "$PWD/build/TestGFFParse" "$PWD/check-original"
g++ %{optflags} -UNDEBUG -std=c++14 -I%{buildroot}%{_includedir} \
    src/TestGFFParse.cpp %{buildroot}%{_libdir}/libgff.a -o staged-parser
bash check-parser.sh "$PWD/staged-parser" "$PWD/check-staged"

%files
%license BoostLicense.txt
%doc Readme.md

%files devel
%{_includedir}/*.h
%{_includedir}/*.hh
%{_libdir}/libgff.a
%{_libdir}/libgff/
%{_datadir}/libgff/

%changelog
* Thu Oct 15 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 2.0.1-1
- Pin official stable source; preserve default parser and static library.
