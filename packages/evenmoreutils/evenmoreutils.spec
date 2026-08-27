# SPDX-License-Identifier: Apache-2.0
Name:           evenmoreutils
Version:        0.6.0
Release:        1%{?dist}
Summary:        A collection of command line tools to extend the shell environment.
License:        GPL-2.0-or-later
URL:            https://github.com/rudymatela/evenmoreutils
Source0:        evenmoreutils-0.6.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A collection of command line tools to extend the shell environment.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.0-1
- Initial openEuler RISC-V package from the full package inventory.
