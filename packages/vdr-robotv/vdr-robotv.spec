# SPDX-License-Identifier: Apache-2.0
Name:           vdr-robotv
Version:        0.15.0
Release:        2%{?dist}
Summary:        VDR server plugin for roboTV
License:        GPL-2.0-or-later
URL:            https://github.com/pipelka/vdr-plugin-robotv
Source0:        vdr-robotv-0.15.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
VDR server plugin for roboTV

%prep
%autosetup -n vdr-plugin-robotv-%{version} -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.15.0-2
- Use the verified upstream archive root during source preparation.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.15.0-1
- Initial openEuler RISC-V package from the full package inventory.
