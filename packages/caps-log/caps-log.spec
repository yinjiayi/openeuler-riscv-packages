# SPDX-License-Identifier: Apache-2.0
Name:           caps-log
Version:        1.2.1
Release:        3%{?dist}
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
  -DBUILD_SHARED_LIBS=OFF \
  -DCAPS_LOG_BUILD_TESTS=ON \
  -DCAPS_LOG_VERSION=%{version} \
  -DINSTALL_GTEST=OFF
%cmake_build

%install
%cmake_install

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files
%{_bindir}/caps-log
%license LICENCE
%doc README.md

%changelog
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.1-3
- Link the FetchContent FTXUI libraries statically so the installed binary is self-contained.
- Keep bundled GoogleTest development files out of the runtime package and use an explicit file list.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.1-2
- Declare the Boost, OpenSSL, libgit2, and source-fetch dependencies required by CMake.
- Configure the explicit build directory, upstream version, and test suite.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.1-1
- Initial openEuler RISC-V package from the full package inventory.
