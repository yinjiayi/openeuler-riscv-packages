# SPDX-License-Identifier: Apache-2.0
Name:           udftools
Version:        2.3
Release:        1%{?dist}
Summary:        Linux tools for UDF filesystems and DVD/CD-R(W) drives
License:        GPL-2.0-or-later
URL:            https://github.com/pali/udftools
Source0:        udftools-2.3.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Linux tools for UDF filesystems and DVD/CD-R(W) drives

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
%doc README
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3-1
- Initial openEuler RISC-V package from the full package inventory.
