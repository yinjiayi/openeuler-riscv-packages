# SPDX-License-Identifier: Apache-2.0
Name: audiofile
Version: 0.3.6
Release: 5%{?dist}
Summary: Library for reading and writing audio files
License: LGPL-2.1-or-later AND GPL-2.0-or-later
URL: https://github.com/mpruett/audiofile
Source0: audiofile-%{version}.tar.gz
Patch0: 0001-fix-negative-left-shift.patch
BuildRequires: alsa-lib-devel
BuildRequires: flac-devel
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libtool
BuildRequires: make
BuildRequires: pkgconf

%description
audiofile provides a uniform API for reading and writing common audio formats.

%package devel
Summary: Development files for audiofile
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, shared-library link, and pkg-config metadata for audiofile.

%prep
%autosetup -p1 -n audiofile-%{version}

%build
%configure --enable-flac
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la %{buildroot}%{_libdir}/*.a

%check
%make_build check

%files
%license COPYING COPYING.GPL
%doc ACKNOWLEDGEMENTS AUTHORS ChangeLog NEWS README
%{_bindir}/sfconvert
%{_bindir}/sfinfo
%{_libdir}/libaudiofile.so.1*
%{_mandir}/man1/sfconvert.1*
%{_mandir}/man1/sfinfo.1*

%files devel
%{_includedir}/audiofile.h
%{_includedir}/af_vfs.h
%{_includedir}/aupvlist.h
%{_libdir}/libaudiofile.so
%{_libdir}/pkgconfig/audiofile.pc
%{_mandir}/man3/*

%changelog
* Wed Sep 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.6-5
- Own the installed public virtual-file header in the development subpackage.

* Wed Sep 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.6-4
- Build the internal static archive required by the upstream unit-test link.
- Remove the static archive from the installed package after the test-capable build.

* Tue Sep 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.6-3
- Build from the official release archive with its generated manuals.
- Package the installed API manual pages in the development subpackage.

* Tue Sep 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.6-2
- Add the ALSA development dependency required by the upstream Linux example.

* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.6-1
- Initial openEuler RISC-V package from frozen lineage and official source evidence.
