# SPDX-License-Identifier: Apache-2.0
Name:           libxmi
Version:        1.2
Release:        1%{?dist}
Summary:        A library for rasterizing 2-D vector graphics
License:        GPL-2.0-or-later
URL:            https://www.gnu.org/software/libxmi/
Source0:        libxmi-1.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make


%description
A library for rasterizing 2-D vector graphics

%package devel
Summary:        Development files for libxmi
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header and unversioned shared-library link for developing applications with libxmi.

%prep
%autosetup -p1
# Autoconf 2.13 emitted an implicit-int compiler probe that GCC 14 rejects.
sed -i 's/^main(){return(0);}$/int main(void){return 0;}/' configure
# GCC 14 rejects the omitted exit(3) declaration.
sed -i '/#include "mi_api.h"/i #include <stdlib.h>' mi_alloc.c

%build
%configure --disable-static
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
%make_build check

%files
%license COPYING
%doc AUTHORS
%doc ChangeLog
%doc NEWS
%doc README
%{_libdir}/libxmi.so.0*

%files devel
%license COPYING
%{_includedir}/xmi.h
%{_libdir}/libxmi.so

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2-1
- Initial openEuler RISC-V package from the full package inventory.
