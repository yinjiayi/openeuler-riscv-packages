# SPDX-License-Identifier: Apache-2.0
Name:           pdbg
Version:        3.6
Release:        1%{?dist}
Summary:        PowerPC FSI Debugger
License:        Apache-2.0
URL:            https://github.com/open-power/pdbg
Source0:        pdbg-3.6.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
PowerPC FSI Debugger

%prep
%autosetup -p1

%build
autoreconf -fi
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
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.6-1
- Initial openEuler RISC-V package from the full package inventory.
