# SPDX-License-Identifier: Apache-2.0
Name:           mtools
Version:        4.0.49
Release:        1%{?dist}
Summary:        A collection of utilities to access MS-DOS disks
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/mtools/
Source0:        mtools-4.0.49.tar.lz
BuildRequires:  gcc
BuildRequires:  lzip
BuildRequires:  make
BuildRequires:  libX11-devel


%description
A collection of utilities to access MS-DOS disks

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files
%license COPYING
%doc NEWS
%doc README
%{_bindir}/*
%{_infodir}/mtools.info*
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.0.49-1
- Initial openEuler RISC-V package from the full package inventory.
