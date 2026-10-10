# SPDX-License-Identifier: Apache-2.0
Name:           cbmconvert
Version:        2.1.6
Release:        1%{?dist}
Summary:        Create, extract and convert 8-bit Commodore binary archives
License:        GPL-2.0-or-later
URL:            https://github.com/dr-m/cbmconvert
Source0:        cbmconvert-2.1.6.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Create, extract and convert 8-bit Commodore binary archives

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.6-1
- Initial openEuler RISC-V package from the full package inventory.
