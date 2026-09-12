# SPDX-License-Identifier: Apache-2.0
Name:           inyokaedit
Version:        0.28.4
Release:        1%{?dist}
Summary:        Editor for Inyoka based portals
License:        GPL-3.0-or-later
URL:            https://github.com/inyokaproject/inyokaedit
Source0:        inyokaedit-0.28.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Editor for Inyoka based portals

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
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.28.4-1
- Initial openEuler RISC-V package from the full package inventory.
