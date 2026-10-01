# SPDX-License-Identifier: Apache-2.0
Name:           conky
Version:        1.24.0
Release:        1%{?dist}
Summary:        A System Monitor
License:        GPL-3.0-or-later
URL:            https://github.com/brndnmtthws/conky
Source0:        conky-1.24.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A System Monitor

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
%license COPYING
%license LICENSE.BSD
%license LICENSE.md
%doc README.md
%doc AUTHORS

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.24.0-1
- Initial openEuler RISC-V package from the full package inventory.
