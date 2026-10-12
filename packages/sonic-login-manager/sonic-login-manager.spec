# SPDX-License-Identifier: Apache-2.0
Name:           sonic-login-manager
Version:        6.7.3
Release:        1%{?dist}
Summary:        Sonic Login Manager
License:        GPL-2.0-or-later
URL:            https://github.com/Sonic-DE/sonic-login-manager
Source0:        sonic-login-manager-6.7.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Sonic Login Manager

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%license LICENSE.CC-BY-3.0
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.7.3-1
- Initial openEuler RISC-V package from the full package inventory.
