# SPDX-License-Identifier: Apache-2.0
Name:           grive
Version:        0.5.3
Release:        1%{?dist}
Summary:        An open source Linux client for Google Drive with support for the new Drive REST API and partial sync
License:        GPL-2.0-or-later
URL:            https://github.com/vitalif/grive2
Source0:        grive-0.5.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
An open source Linux client for Google Drive with support for the new Drive REST API and partial sync

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.5.3-1
- Initial openEuler RISC-V package from the full package inventory.
