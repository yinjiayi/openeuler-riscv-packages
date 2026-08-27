# SPDX-License-Identifier: Apache-2.0
Name:           rf24
Version:        1.5.0
Release:        1%{?dist}
Summary:        Linux support for RF24 radio modules
License:        GPL-2.0-or-later
URL:            https://github.com/nRF24/RF24
Source0:        rf24-1.5.0.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Linux support for RF24 radio modules

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
%license LICENSE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.0-1
- Initial openEuler RISC-V package from the full package inventory.
