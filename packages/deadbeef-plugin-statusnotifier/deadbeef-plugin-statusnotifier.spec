# SPDX-License-Identifier: Apache-2.0
Name:           deadbeef-plugin-statusnotifier
Version:        1.6
Release:        1%{?dist}
Summary:        plugin for DeaDBeeF that replaces its default tray icon with one that supports the StatusNotifierIitem protocol
License:        GPL-3.0-or-later
URL:            https://github.com/vovochka404/deadbeef-statusnotifier-plugin
Source0:        deadbeef-plugin-statusnotifier-1.6.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
plugin for DeaDBeeF that replaces its default tray icon with one that supports the StatusNotifierIitem protocol

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
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6-1
- Initial openEuler RISC-V package from the full package inventory.
