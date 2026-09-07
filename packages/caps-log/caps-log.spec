# SPDX-License-Identifier: Apache-2.0
Name:           caps-log
Version:        1.2.1
Release:        2%{?dist}
Summary:        A small, terminal-based journaling tool
License:        MIT
URL:            https://github.com/NikolaDucak/caps-log
Source0:        caps-log-1.2.1.tar.gz
BuildRequires:  boost-devel
BuildRequires:  boost-program-options
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  libgit2-devel
BuildRequires:  make
BuildRequires:  openssl-devel

%description
A small, terminal-based journaling tool

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} \
  -DCAPS_LOG_BUILD_TESTS=ON \
  -DCAPS_LOG_VERSION=%{version}
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENCE
%doc README.md

%changelog
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.1-2
- Declare the Boost, OpenSSL, libgit2, and source-fetch dependencies required by CMake.
- Configure the explicit build directory, upstream version, and test suite.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.1-1
- Initial openEuler RISC-V package from the full package inventory.
