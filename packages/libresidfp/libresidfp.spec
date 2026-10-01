# SPDX-License-Identifier: Apache-2.0
Name:           libresidfp
Version:        1.2.0
Release:        1%{?dist}
Summary:        Cycle exact SID emulation
License:        GPL-2.0-or-later
URL:            https://github.com/libsidplayfp/libresidfp
Source0:        libresidfp-1.2.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
Cycle exact SID emulation

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
%doc NEWS.md
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.0-1
- Initial openEuler RISC-V package from the full package inventory.
