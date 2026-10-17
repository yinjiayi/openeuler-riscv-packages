# SPDX-License-Identifier: LGPL-2.1-or-later
# Copyright (c) 2026 yinjiayi
# Default build is seven static archives; no separate ELF debuginfo product.
# Preserve distribution -g and compiler flags in the actual archives.
%global debug_package %{nil}
%global upstream_commit c3762283e2fffe795cc1462289f0da40834acb8a
Name:           libclaw
Version:        1.9.1
Release:        1%{?dist}
Summary:        General-purpose modular C++ library
License:        LGPL-2.1-or-later AND gnuplot
URL:            https://github.com/j-jorge/libclaw
Source0:        https://codeload.github.com/j-jorge/libclaw/tar.gz/%{upstream_commit}#/libclaw-%{version}.tar.gz
Source1:        https://ftp.gnu.org/gnu/Licenses/gpl-2.0.txt#/GPL-2.0.txt
Source2:        https://raw.githubusercontent.com/spdx/license-list-data/d46e94e2c78ceede1cfc63cfa0396472d2798d4c/text/gnuplot.txt
Source3:        https://raw.githubusercontent.com/j-jorge/libclaw/%{upstream_commit}/.gitattributes
Source4:        https://raw.githubusercontent.com/j-jorge/libclaw/%{upstream_commit}/.gitignore
Patch0:         0001-multilib-CMake-config.patch
Patch1:         0002-add-installed-QA.patch
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gettext
BuildRequires:  gettext-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  zlib-devel
BuildRequires:  glibc-devel
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  grep
BuildRequires:  findutils
BuildRequires:  binutils

%description
Claw provides core algorithms and containers, logging, application arguments,
configuration files, dynamic loading, image formats, networking and tweening.
Retains the original default seven static archives, header-only core, complete
HTML documentation, French localization and all 21 example source archives.
The library is LGPL2.1-or-later. A conservative gnuplot permission companion
covers only the retained save-generated example plot configuration banner.

%package tests
Summary:        Complete original installed-example suite and consumer
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc
Requires:       gcc-c++
Requires:       cmake
Requires:       make
Requires:       gettext-devel
Requires:       libjpeg-turbo-devel
Requires:       libpng-devel
Requires:       zlib-devel
Requires:       glibc-devel
Requires:       bash
Requires:       coreutils
Requires:       grep
Requires:       findutils
Requires:       tar
Requires:       gzip
Requires:       binutils
Requires:       rpm

%description tests
Runs the unchanged original check-examples.sh to compile all 21 installed
example archives and strictly checks 21 passes and zero failures. A separate
downstream installed CMake/API consumer does not replace the original suite.

%prep
%setup -q -n %{name}-%{upstream_commit}
install -m 0644 %{SOURCE3} .gitattributes
install -m 0644 %{SOURCE4} .gitignore
%patch0 -p1
%patch1 -p1
install -d distribution-licenses
install -m 0644 %{SOURCE1} distribution-licenses/GPL-2.0.txt
install -m 0644 %{SOURCE2} distribution-licenses/gnuplot.txt
(cd test && sha256sum check-examples.sh) > downstream/SHA256SUMS

%build
cmake -S cmake -B build \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=lib64 \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_CXX_FLAGS="%{optflags}" \
    -DCLAW_BUILD_LOCALIZATION=ON \
    -DCLAW_BUILD_DOCUMENTATION=ON \
    -DCLAW_BUILD_EXAMPLES=ON
cmake --build build --parallel %{?_smp_build_ncpus}
for feature in LOCALIZATION DOCUMENTATION EXAMPLES; do
    grep -Fx "CLAW_BUILD_${feature}:BOOL=ON" build/CMakeCache.txt
done
test -s build/doc/html/index.html

%install
DESTDIR=%{buildroot} cmake --install build
install -d %{buildroot}%{_datadir}/%{name}/original
install -m 0644 test/check-examples.sh %{buildroot}%{_datadir}/%{name}/original/
install -m 0644 downstream/SHA256SUMS downstream/consumer.cpp downstream/CMakeLists.txt \
    %{buildroot}%{_datadir}/%{name}/
install -m 0755 downstream/run-tests.sh %{buildroot}%{_datadir}/%{name}/run-tests.sh

%check
bash %{buildroot}%{_datadir}/%{name}/run-tests.sh --staged %{buildroot}

%files
%license COPYING distribution-licenses/
%doc README.md
%{_includedir}/claw/
%{_libdir}/libclaw_*.a
%{_libdir}/cmake/claw/
%{_datadir}/doc/libclaw1/
%{_datadir}/locale/fr/LC_MESSAGES/libclaw.mo

%files tests
%{_datadir}/%{name}/

%changelog
* Sun Oct 18 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.9.1-1
- Package fixed upstream tag with unchanged default features and original suite.
- Honor multilib CMake config directory and add separate installed consumer.
