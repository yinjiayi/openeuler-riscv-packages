# SPDX-License-Identifier: Apache-2.0
Name:           cctag
Version:        1.0.4
Release:        1%{?dist}
Summary:        Detection of CCTag markers made up of concentric circles.
License:        MPL-2.0
URL:            https://github.com/alicevision/CCTag
Source0:        cctag-1.0.4.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Detection of CCTag markers made up of concentric circles.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license COPYING.md
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.4-1
- Initial openEuler RISC-V package from the full package inventory.
