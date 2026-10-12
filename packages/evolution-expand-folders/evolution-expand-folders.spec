# SPDX-License-Identifier: Apache-2.0
Name:           evolution-expand-folders
Version:        1.0.0
Release:        1%{?dist}
Summary:        Evolution plugin adding expand/collapse for the mail folder tree, via context menu and keyboard shortcuts
License:        LGPL-2.1-or-later
URL:            https://github.com/christiansacks/evolution-expand-folders
Source0:        evolution-expand-folders-1.0.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Evolution plugin adding expand/collapse for the mail folder tree, via context menu and keyboard shortcuts

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
