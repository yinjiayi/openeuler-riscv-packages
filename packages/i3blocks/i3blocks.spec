# SPDX-License-Identifier: Apache-2.0
Name:           i3blocks
Version:        1.5
Release:        1%{?dist}
Summary:        Define blocks for your i3bar status line
License:        GPL-3.0-or-later
URL:            https://github.com/vivien/i3blocks
Source0:        i3blocks-1.5.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Define blocks for your i3bar status line

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


%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5-1
- Initial openEuler RISC-V package from the full package inventory.
