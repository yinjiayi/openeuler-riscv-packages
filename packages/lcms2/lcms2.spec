# SPDX-License-Identifier: Apache-2.0
Name:           lcms2
Version:        2.19.1
Release:        1%{?dist}
Summary:        Small-footprint color management engine
License:        MIT AND GPL-3.0-or-later
URL:            https://www.littlecms.com/
Source0:        lcms2-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libtiff-devel
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf
BuildRequires:  zlib-devel

%description
Little CMS is a small-footprint, speed-optimized color management engine.
This package contains its runtime library.

%package utils
Summary:        Command-line utilities for Little CMS
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description utils
Color-profile linking, conversion, PostScript, JPEG, and TIFF utilities.

%package devel
Summary:        Development files for Little CMS
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, pkg-config metadata, and the unversioned linker name for Little CMS.

%package help
Summary:        Documentation for Little CMS utilities
BuildArch:      noarch

%description help
Manual pages and upstream release documentation for Little CMS.

%prep
%autosetup -p1

%build
%meson \
  -Dfastfloat=false \
  -Djpeg=enabled \
  -Dtests=enabled \
  -Dthreaded=false \
  -Dtiff=enabled \
  -Dutils=true
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license LICENSE
%{_libdir}/liblcms2.so.2*

%files utils
%license LICENSE
%{_bindir}/jpgicc
%{_bindir}/linkicc
%{_bindir}/psicc
%{_bindir}/tificc
%{_bindir}/tifdiff
%{_bindir}/transicc

%files devel
%license LICENSE
%{_includedir}/lcms2.h
%{_includedir}/lcms2_plugin.h
%{_libdir}/liblcms2.so
%{_libdir}/pkgconfig/lcms2.pc

%files help
%license LICENSE
%doc AUTHORS ChangeLog README.md
%{_mandir}/man1/jpgicc.1*
%{_mandir}/man1/linkicc.1*
%{_mandir}/man1/psicc.1*
%{_mandir}/man1/tificc.1*
%{_mandir}/man1/transicc.1*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.19.1-1
- Initial openEuler RISC-V package from frozen cross-distribution and upstream evidence.
