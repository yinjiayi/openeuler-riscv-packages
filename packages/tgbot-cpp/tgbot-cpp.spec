# SPDX-License-Identifier: Apache-2.0
Name:           tgbot-cpp
Version:        1.6
Release:        2%{?dist}
Summary:        C++ library for Telegram bot API
License:        MIT
URL:            https://github.com/reo7sp/tgbot-cpp
Source0:        tgbot-cpp-1.6.tar.gz
BuildRequires:  boost-devel
BuildRequires:  boost-system
BuildRequires:  boost-test
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libcurl-devel
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel

%description
C++ library for Telegram bot API

%prep
%autosetup -p1

%build
%cmake -DENABLE_TESTS=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Mon Aug 31 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6-2
- Add the dependencies required by the upstream CMake configuration.
- Enable the upstream test suite with its actual ENABLE_TESTS option.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6-1
- Initial openEuler RISC-V package from the full package inventory.
