# SPDX-License-Identifier: Apache-2.0
Name:           mdk4
Version:        4.2
Release:        1%{?dist}
Summary:        A tool to exploit common IEEE 802.11 protocol weaknesses
License:        GPL-3.0-or-later
URL:            https://github.com/aircrack-ng/mdk4
Source0:        mdk4-4.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A tool to exploit common IEEE 802.11 protocol weaknesses

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
%license COPYING
%doc README.md
%doc AUTHORS
%doc CHANGELOG

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.2-1
- Initial openEuler RISC-V package from the full package inventory.
