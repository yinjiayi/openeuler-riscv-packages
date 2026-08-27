# SPDX-License-Identifier: Apache-2.0
Name:           xclip
Version:        0.13
Release:        1%{?dist}
Summary:        Command line interface to the X11 clipboard
License:        GPL-2.0-or-later
URL:            https://github.com/astrand/xclip
Source0:        xclip-0.13.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Command line interface to the X11 clipboard

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
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.13-1
- Initial openEuler RISC-V package from the full package inventory.
