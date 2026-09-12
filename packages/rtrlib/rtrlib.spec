# SPDX-License-Identifier: Apache-2.0
Name:           rtrlib
Version:        0.8.0
Release:        2%{?dist}
Summary:        RPKI-RTR client library
License:        MIT
URL:            https://github.com/rtrlib/rtrlib
Source0:        rtrlib-0.8.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  libcmocka-devel
BuildRequires:  libssh-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
RPKI-RTR client library

%prep
%autosetup -p1

%build
%cmake_conf \
  -DRTRLIB_TRANSPORT_SSH=ON \
  -DUNIT_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure --no-tests=error

%files -f %{name}.files
%license LICENSE
%doc README.md
%doc CHANGELOG

%changelog
* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.0-2
- Use the openEuler out-of-source CMake workflow, retain SSH, and run all tests.

* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.0-1
- Initial openEuler RISC-V package from the full package inventory.
