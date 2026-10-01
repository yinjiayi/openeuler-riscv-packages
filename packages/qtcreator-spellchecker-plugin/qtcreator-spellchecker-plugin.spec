# SPDX-License-Identifier: Apache-2.0
Name:           qtcreator-spellchecker-plugin
Version:        3.12.1
Release:        1%{?dist}
Summary:        Spell Checker plugin for the Qt Creator IDE
License:        LGPL-3.0-or-later
URL:            https://github.com/CJCombrink/SpellChecker-Plugin
Source0:        qtcreator-spellchecker-plugin-3.12.1.tar.gz
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
%license COPYING
%license COPYING.LESSER
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.12.1-1
- Initial openEuler RISC-V package from the full package inventory.
