# SPDX-License-Identifier: Apache-2.0
Name:           xoreos-tools
Version:        0.0.6
Release:        1%{?dist}
Summary:        Tools to help with xoreos development
License:        GPL-3.0-or-later
URL:            https://github.com/xoreos/xoreos-tools
Source0:        xoreos-tools-0.0.6.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Tools to help with xoreos development

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
%doc NEWS.md
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.6-1
- Initial openEuler RISC-V package from the full package inventory.
