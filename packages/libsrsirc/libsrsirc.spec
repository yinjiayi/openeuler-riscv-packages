# SPDX-License-Identifier: Apache-2.0
Name:           libsrsirc
Version:        0.0.14.1
Release:        1%{?dist}
Summary:        A lightweight IRC library (includes icat)
License:        BSD-3-Clause
URL:            https://github.com/fstd/libsrsirc
Source0:        libsrsirc-0.0.14.1.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A lightweight IRC library (includes icat)

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.14.1-1
- Initial openEuler RISC-V package from the full package inventory.
