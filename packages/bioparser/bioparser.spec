# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
# Header-only payload and source-only installed QA: no installed ELF to split.
%global debug_package %{nil}
%global upstream_commit 4fa7126293d2a0eb90125b58fb704f0eed33ffe0
%global biosoup_commit 3e31aa1d9039a2689241aebd18c45933b2d0f5e3
Name:           bioparser
Version:        3.1.0
Release:        1%{?dist}
Summary:        Header-only parsers for bioinformatics text and gzip formats
License:        MIT
URL:            https://github.com/rvaser/bioparser
Source0:        https://codeload.github.com/rvaser/bioparser/tar.gz/%{upstream_commit}#/bioparser-%{version}.tar.gz
Source1:        https://codeload.github.com/rvaser/biosoup/tar.gz/%{biosoup_commit}#/biosoup-0.11.0.tar.gz
Patch0:         0001-add-installed-QA.patch
BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.11
BuildRequires:  make
BuildRequires:  gtest-devel >= 1.10.0
BuildRequires:  zlib-devel >= 1.2.8
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  grep
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  patch
BuildRequires:  python3
BuildRequires:  rpm
Requires:       zlib-devel >= 1.2.8

%description
Bioparser provides C++ parsers for FASTA, FASTQ, MHAP, PAF and SAM, including
gzip inputs. This header-only package includes its relocatable CMake exports.
All original defaults and all 35 original GoogleTest cases are preserved.
Biosoup is an offline, fixed upstream test-only subproject, not a public API
provided by this RPM. No upstream source or original test body is patched.

%package tests
Summary:        Complete original Bioparser test sources, fixtures and installed QA
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc-c++
Requires:       cmake >= 3.11
Requires:       make
Requires:       gtest-devel >= 1.10.0
Requires:       zlib-devel >= 1.2.8
Requires:       bash
Requires:       coreutils
Requires:       findutils
Requires:       grep
Requires:       python3
Requires:       rpm

%description tests
Rebuild all six unchanged upstream test translation units against the installed
Bioparser CMake target and run all 35 cases on all ten original fixtures.
The test-only Biosoup headers remain private. An independent installed consumer
adds plain/gzip and reset checks; it does not replace the original suite.
No test executable, compiler output or architecture-specific generated header
is shipped. Biosoup's own timing tests are not Bioparser's default suite.

%prep
%setup -q -n %{name}-%{upstream_commit}
tar -xzf %{SOURCE1}
%patch0 -p1

%build
cmake -S . -B build \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=lib64 \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_CXX_FLAGS_RELWITHDEBINFO="%{optflags} -UNDEBUG" \
    -DFETCHCONTENT_SOURCE_DIR_BIOSOUP="$PWD/biosoup-%{biosoup_commit}" \
    -DFETCHCONTENT_FULLY_DISCONNECTED=ON \
    -DCMAKE_REQUIRE_FIND_PACKAGE_GTest=ON
# Original top-level options must retain both enabled defaults.
grep -Fx 'bioparser_install:BOOL=ON' build/CMakeCache.txt
grep -Fx 'bioparser_build_tests:BOOL=ON' build/CMakeCache.txt
# These are the original defaults for an embedded Biosoup subproject.
grep -Fx 'biosoup_install:BOOL=OFF' build/CMakeCache.txt
grep -Fx 'biosoup_build_tests:BOOL=OFF' build/CMakeCache.txt
cmake --build build --parallel %{?_smp_build_ncpus}
test -x build/bin/bioparser_test

%install
DESTDIR=%{buildroot} cmake --install build
install -d %{buildroot}%{_datadir}/%{name}/qa/tests/data %{buildroot}%{_datadir}/%{name}/qa/biosoup/include
install -m 0644 test/*_test.cpp test/bioparser_test_config.h.in %{buildroot}%{_datadir}/%{name}/qa/tests/
install -m 0644 test/data/* %{buildroot}%{_datadir}/%{name}/qa/tests/data/
cp -a biosoup-%{biosoup_commit}/include/biosoup %{buildroot}%{_datadir}/%{name}/qa/biosoup/include/
install -m 0644 downstream/CMakeLists.txt downstream/consumer.cpp downstream/check-results.py downstream/UPSTREAM-NOTICES %{buildroot}%{_datadir}/%{name}/qa/
install -m 0755 downstream/run-tests.sh %{buildroot}%{_datadir}/%{name}/qa/

%check
# Clear filtering/shuffling/repetition injections before the unchanged suite.
for key in $(env | cut -d= -f1 | grep '^GTEST_' || :); do unset "$key"; done
build/bin/bioparser_test --gtest_filter='*' --gtest_output=xml:original-results.xml
python3 downstream/check-results.py original-results.xml
# Compute after install post-processing; this is integrity, not a signature.
(cd %{buildroot}%{_datadir}/%{name}/qa && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 sha256sum) > %{buildroot}%{_datadir}/%{name}/qa/SHA256SUMS
bash %{buildroot}%{_datadir}/%{name}/qa/run-tests.sh --staged %{buildroot}
test "$(find %{buildroot}%{_includedir}/bioparser -type f | wc -l)" -eq 6
test "$(find %{buildroot}%{_datadir}/%{name}/qa/tests/data -type f | wc -l)" -eq 10

%files
%license LICENSE downstream/UPSTREAM-NOTICES
%doc README.md
%{_includedir}/bioparser/
%{_libdir}/cmake/bioparser/

%files tests
%license LICENSE downstream/UPSTREAM-NOTICES
%{_datadir}/%{name}/

%changelog
* Sun Oct 18 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 3.1.0-1
- Pin both official MIT sources and retain all original Bioparser tests/defaults.
- Add separate installed-target replay without public Biosoup namespace claims.
