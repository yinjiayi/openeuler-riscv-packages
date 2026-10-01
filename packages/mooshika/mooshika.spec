# SPDX-License-Identifier: Apache-2.0
Name:           mooshika
Version:        1.1
Release:        1%{?dist}
Summary:        RDMA abstraction layer
License:        LGPL-3.0-or-later
URL:            https://github.com/martinetd/mooshika
Source0:        mooshika-1.1.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
RDMA abstraction layer

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
%license LICENSE
%doc README.md
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1-1
- Initial openEuler RISC-V package from the full package inventory.
