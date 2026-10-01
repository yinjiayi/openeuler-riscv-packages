# SPDX-License-Identifier: Apache-2.0
Name:           qtcreator-discord-rich-presence-plugin
Version:        1.0.3
Release:        1%{?dist}
Summary:        Spell Checker plugin for the Qt Creator IDE
License:        GPL-3.0-or-later
URL:            https://github.com/TheBill2001/qtcreator-discord-rich-presence-plugin
Source0:        qtcreator-discord-rich-presence-plugin-1.0.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Spell Checker plugin for the Qt Creator IDE

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
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.3-1
- Initial openEuler RISC-V package from the full package inventory.
