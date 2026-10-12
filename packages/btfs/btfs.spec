# SPDX-License-Identifier: Apache-2.0
Name:           btfs
Version:        3.1
Release:        1%{?dist}
Summary:        A bittorrent filesystem based on FUSE
License:        GPL-3.0-or-later
URL:            https://github.com/johang/btfs
Source0:        btfs-3.1.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
A bittorrent filesystem based on FUSE

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

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.1-1
- Initial openEuler RISC-V package from the full package inventory.
