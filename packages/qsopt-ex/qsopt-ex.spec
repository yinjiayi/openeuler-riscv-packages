# SPDX-License-Identifier: Apache-2.0
Name:           qsopt-ex
Version:        2.5.10.3
Release:        1%{?dist}
Summary:        Exact linear programming solver
License:        GPL-3.0-or-later
URL:            https://github.com/jonls/qsopt-ex
Source0:        qsopt-ex-2.5.10.3.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Exact linear programming solver

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
%license License.txt
%doc README.md
%doc NEWS.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.5.10.3-1
- Initial openEuler RISC-V package from the full package inventory.
