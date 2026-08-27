# SPDX-License-Identifier: Apache-2.0
Name:           chsrc
Version:        0.2.6
Release:        1%{?dist}
Summary:        A cli tool to change source for every software on every platform
License:        GPL-3.0-or-later
URL:            https://github.com/RubyMetric/chsrc
Source0:        chsrc-0.2.6.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A cli tool to change source for every software on every platform

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.6-1
- Initial openEuler RISC-V package from the full package inventory.
