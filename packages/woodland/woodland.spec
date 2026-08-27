# SPDX-License-Identifier: Apache-2.0
Name:           woodland
Version:        2.1.1
Release:        1%{?dist}
Summary:        minimal Wayland compositor based on wlroots
License:        GPL-2.0-or-later
URL:            https://github.com/DiogenesN/woodland
Source0:        woodland-2.1.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
minimal Wayland compositor based on wlroots

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
%license LICENSE.txt
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.1-1
- Initial openEuler RISC-V package from the full package inventory.
