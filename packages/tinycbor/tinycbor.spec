# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
%global upstream_commit 6442e749ca811e24afad1551338a45c75e09808f
Name:           tinycbor
Version:        7.0
Release:        1%{?dist}
Summary:        Compact CBOR encoder, decoder and diagnostic tool
License:        MIT
URL:            https://github.com/intel/tinycbor
Source0:        https://codeload.github.com/intel/tinycbor/tar.gz/%{upstream_commit}#/tinycbor-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/intel/tinycbor/%{upstream_commit}/.gitattributes#/upstream-gitattributes
Source2:        https://raw.githubusercontent.com/intel/tinycbor/%{upstream_commit}/.gitignore#/upstream-gitignore
Source3:        https://raw.githubusercontent.com/intel/tinycbor/%{upstream_commit}/tests/.gitignore#/upstream-tests-gitignore
Patch0:         0001-correct-pkgconfig-install-paths.patch
Patch1:         0002-add-installed-QA.patch
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.10
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  qt6-qtbase-devel
BuildRequires:  pkgconfig(libcjson)
BuildRequires:  glibc-devel
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  rpm
BuildRequires:  binutils
BuildRequires:  grep
BuildRequires:  findutils
BuildRequires:  diffutils
BuildRequires:  patch
BuildRequires:  sed
BuildRequires:  gawk
BuildRequires:  tar
BuildRequires:  gzip

%description
TinyCBOR encodes and parses Concise Binary Object Representation data. This
recipe retains the original static library, floating-point support, CBOR-to-JSON
conversion and tools. Tests are explicitly enabled and Qt6 and cJSON are
mandatory build inputs. Upstream project/header/pkg-config version is 7.0;
the separate upstream shared-library VERSION expression is 0.7.0.

%package devel
Summary:        TinyCBOR headers, static archive and development metadata
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, the original default static archive, pkg-config and relocatable CMake
exports. No default library feature or compiler warning is disabled.

%package tests
Summary:        Complete original TinyCBOR test programs and installed QA
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       gcc
Requires:       gcc-c++
Requires:       cmake >= 3.10
Requires:       make
Requires:       pkgconf-pkg-config
Requires:       glibc-devel
Requires:       bash
Requires:       coreutils
Requires:       rpm
Requires:       binutils
Requires:       grep
Requires:       findutils
Requires:       diffutils

%description tests
All five original test executables: C90 and C++ compilation contracts, encoder,
parser and JSON conversion. The original Qt data-row skips are retained. The
built json2cbor tool is retained here for installed CLI QA; upstream builds it
but does not install it. Additional installed C/pkg-config and CMake consumers
do not replace the original tests and are not an upstream test suite.

%prep
%setup -q -n %{name}-%{upstream_commit}
install -m 0644 %{SOURCE1} .gitattributes
install -m 0644 %{SOURCE2} .gitignore
install -m 0644 %{SOURCE3} tests/.gitignore
%patch0 -p1
%patch1 -p1

%build
pkg-config --exists 'libcjson'
cmake -S . -B build \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=lib64 \
    -DCMAKE_INSTALL_INCLUDEDIR=include \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_C_FLAGS_RELWITHDEBINFO="%{optflags} -UNDEBUG" \
    -DCMAKE_CXX_FLAGS_RELWITHDEBINFO="%{optflags} -UNDEBUG" \
    -DBUILD_TESTING:BOOL=ON \
    -DCMAKE_REQUIRE_FIND_PACKAGE_Qt6=ON
cmake --build build --parallel %{?_smp_build_ncpus}
for feature in BUILD_TESTING WITH_FLOATING_POINT WITH_CBOR2JSON BUILD_TOOLS WITH_VALGRIND; do
    grep -Fx "${feature}:BOOL=ON" build/CMakeCache.txt
done
for feature in WITH_FREESTANDING BUILD_EXAMPLES; do
    grep -Fx "${feature}:BOOL=OFF" build/CMakeCache.txt
done
test -s build/libtinycbor.a
test -x build/tools/json2cbor/json2cbor
test -x build/tools/cbordump/cbordump
# A missing Qt6 must never turn into a successful zero/fewer-tests build.
(cd build && ctest -N) > ctest-registry.txt
grep -Fx 'Total Tests: 5' ctest-registry.txt
for suite in c90 cpp encoder parser tojson; do
    grep -E "Test +#[1-5]: tst_${suite}$" ctest-registry.txt
    test -x "build/tests/${suite}/tst_${suite}"
done

%install
DESTDIR=%{buildroot} cmake --install build
install -d %{buildroot}%{_libexecdir}/%{name} %{buildroot}%{_datadir}/%{name}
for suite in c90 cpp encoder parser tojson; do
    install -m 0755 "build/tests/${suite}/tst_${suite}" %{buildroot}%{_libexecdir}/%{name}/
done
install -m 0755 build/tools/json2cbor/json2cbor %{buildroot}%{_libexecdir}/%{name}/
install -m 0755 downstream/run-tests.sh %{buildroot}%{_datadir}/%{name}/
install -m 0644 downstream/consumer.c downstream/CMakeLists.txt %{buildroot}%{_datadir}/%{name}/
(cd %{buildroot}%{_libexecdir}/%{name} && sha256sum tst_c90 tst_cpp tst_encoder tst_parser tst_tojson json2cbor) > %{buildroot}%{_datadir}/%{name}/SHA256SUMS

%check
# Run the original CTest commands including upstream's optional Valgrind wrapper.
ctest --test-dir build --output-on-failure --no-tests=error
bash %{buildroot}%{_datadir}/%{name}/run-tests.sh --staged %{buildroot}

%files
%license LICENSE downstream/UPSTREAM-NOTICES
%doc README
%{_bindir}/cbordump

%files devel
%license LICENSE downstream/UPSTREAM-NOTICES
%{_includedir}/tinycbor/
%{_libdir}/libtinycbor.a
%{_libdir}/pkgconfig/tinycbor.pc
%{_libdir}/cmake/tinycbor/

%files tests
%license LICENSE downstream/UPSTREAM-NOTICES
%{_libexecdir}/%{name}/
%{_datadir}/%{name}/

%changelog
* Sun Oct 18 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 7.0-1
- Package the fixed official unsigned tag with original features and all tests.
- Correct pkg-config full install paths without changing CMake export semantics.
- Retain complete upstream copyright notices and add installed downstream QA.
