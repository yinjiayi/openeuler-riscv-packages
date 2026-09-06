# SPDX-License-Identifier: Apache-2.0
Name:           libfaketime
Version:        0.9.12
Release:        1%{?dist}
Summary:        Report fake dates and times to programs without having to change the system-wide time.
License:        GPL-2.0-or-later
URL:            https://github.com/wolfcw/libfaketime
Source0:        libfaketime-0.9.12.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Report fake dates and times to programs without having to change the system-wide time.

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
%doc README
%doc NEWS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.12-1
- Initial openEuler RISC-V package from the full package inventory.
