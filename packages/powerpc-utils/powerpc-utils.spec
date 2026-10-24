# SPDX-License-Identifier: Apache-2.0
Name:           powerpc-utils
Version:        1.3.13
Release:        1%{?dist}
Summary:        PERL-based scripts for maintaining and servicing PowerPC systems
License:        GPL-2.0-or-later
URL:            https://github.com/ibm-power-utilities/powerpc-utils
Source0:        powerpc-utils-1.3.13.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
PERL-based scripts for maintaining and servicing PowerPC systems

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

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.13-1
- Initial openEuler RISC-V package from the full package inventory.
