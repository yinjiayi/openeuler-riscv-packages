# SPDX-License-Identifier: Apache-2.0
Name:           wlcs
Version:        1.8.1
Release:        1%{?dist}
Summary:        Canonical's protocol-conformance-verifying test suite for Wayland compositor implementations.
License:        GPL-2.0-or-later
URL:            https://github.com/canonical/wlcs
Source0:        wlcs-1.8.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Canonical's protocol-conformance-verifying test suite for Wayland compositor implementations.

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license COPYING.GPL2
%license COPYING.GPL3
%doc README.rst

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8.1-1
- Initial openEuler RISC-V package from the full package inventory.
