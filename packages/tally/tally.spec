# SPDX-License-Identifier: Apache-2.0
Name:           tally
Version:        0.2.0
Release:        1%{?dist}
Summary:        From-scratch C reimplementation of GNU wc(1); byte-identical, faster on every measured workload
License:        GPL-3.0-or-later
URL:            https://github.com/tenseleyFlow/tally
Source0:        tally-0.2.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
From-scratch C reimplementation of GNU wc(1); byte-identical, faster on every measured workload

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
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.0-1
- Initial openEuler RISC-V package from the full package inventory.
