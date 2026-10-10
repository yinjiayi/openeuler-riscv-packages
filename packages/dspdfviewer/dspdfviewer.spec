# SPDX-License-Identifier: Apache-2.0
Name:           dspdfviewer
Version:        1.15.1
Release:        1%{?dist}
Summary:        Viewer for latex-beamer presentations that are built with the «show notes on second screen»-option
License:        GPL-2.0-or-later
URL:            https://github.com/dannyedel/dspdfviewer
Source0:        dspdfviewer-1.15.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Viewer for latex-beamer presentations that are built with the «show notes on second screen»-option

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.15.1-1
- Initial openEuler RISC-V package from the full package inventory.
