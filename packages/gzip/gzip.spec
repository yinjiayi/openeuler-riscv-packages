# SPDX-License-Identifier: Apache-2.0
Name:           gzip
Version:        1.14
Release:        1%{?dist}
Summary:        GNU data compression utility
License:        GPL-3.0-or-later AND GFDL-1.3-only
URL:            https://www.gnu.org/software/gzip/
Source0:        gzip-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  less
BuildRequires:  make
BuildRequires:  texinfo
Requires:       coreutils

%description
GNU gzip compresses and decompresses files using the widely supported gzip
format and includes the related zgrep, zdiff, zless, and other helper tools.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir
# The uncompress compatibility name is owned by the ncompress package.
rm -f %{buildroot}%{_bindir}/uncompress

%check
%make_build check

%files
%license COPYING doc/fdl.texi
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_bindir}/*
%{_mandir}/man1/*.1*
%{_infodir}/gzip.info*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.14-1
- Initial openEuler RISC-V package from reviewed Fedora 44 and upstream evidence.
