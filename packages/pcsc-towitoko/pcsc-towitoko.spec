# SPDX-License-Identifier: Apache-2.0
Name:           pcsc-towitoko
Version:        2.0.8
Release:        1%{?dist}
Summary:        PCSC driver for Towitoko Smart Card Readers
License:        LGPL-2.1-or-later
URL:            https://github.com/cprados/towitoko-linux
Source0:        pcsc-towitoko-2.0.8.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
PCSC driver for Towitoko Smart Card Readers

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
%license COPYING
%doc README
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.8-1
- Initial openEuler RISC-V package from the full package inventory.
