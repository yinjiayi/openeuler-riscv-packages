# SPDX-License-Identifier: Apache-2.0
Name:           sslscan
Version:        2.2.2
Release:        1%{?dist}
Summary:        Fast tool to scan SSL services such as HTTPS to determine supported ciphers
License:        GPL-3.0-or-later
URL:            https://github.com/rbsec/sslscan
Source0:        sslscan-2.2.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Fast tool to scan SSL services such as HTTPS to determine supported ciphers

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX=%{_prefix}
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build test

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.2-1
- Initial openEuler RISC-V package from the full package inventory.
