# SPDX-License-Identifier: Apache-2.0
Name:           jbigkit
Version:        2.1
Release:        1%{?dist}
Summary:        JBIG1 lossless image compression tools
License:        GPL-2.0-or-later
URL:            https://www.cl.cam.ac.uk/~mgk25/jbigkit/
Source0:        jbigkit-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
JBIG-KIT provides command-line converters between PBM and the JBIG1 image
compression format defined by ISO/IEC 11544 and ITU-T Recommendation T.82.

%package libs
Summary:        JBIG1 lossless image compression libraries

%description libs
Shared libraries implementing the T.82 and T.85 JBIG1 coding interfaces.

%package devel
Summary:        Development files for JBIG-KIT
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Headers and unversioned shared-library links for developing applications with
JBIG-KIT.

%prep
%autosetup -p1

%build
%make_build \
  CC="%{__cc}" \
  CFLAGS="%{optflags} -fPIC -W -Wno-unused-result"

%{__cc} %{optflags} %{build_ldflags} -shared \
  -Wl,-soname,libjbig.so.%{version} \
  -o libjbig/libjbig.so.%{version} \
  libjbig/jbig.o libjbig/jbig_ar.o
%{__cc} %{optflags} %{build_ldflags} -shared \
  -Wl,-soname,libjbig85.so.%{version} \
  -o libjbig/libjbig85.so.%{version} \
  libjbig/jbig85.o libjbig/jbig_ar.o
ln -s libjbig.so.%{version} libjbig/libjbig.so
ln -s libjbig85.so.%{version} libjbig/libjbig85.so

%{__cc} %{optflags} %{build_ldflags} -o pbmtools/pbmtojbg \
  pbmtools/pbmtojbg.o -Llibjbig -ljbig
%{__cc} %{optflags} %{build_ldflags} -o pbmtools/jbgtopbm \
  pbmtools/jbgtopbm.o -Llibjbig -ljbig
%{__cc} %{optflags} %{build_ldflags} -o pbmtools/pbmtojbg85 \
  pbmtools/pbmtojbg85.o -Llibjbig -ljbig85
%{__cc} %{optflags} %{build_ldflags} -o pbmtools/jbgtopbm85 \
  pbmtools/jbgtopbm85.o -Llibjbig -ljbig85

%install
install -Dpm0755 libjbig/libjbig.so.%{version} \
  %{buildroot}%{_libdir}/libjbig.so.%{version}
install -Dpm0755 libjbig/libjbig85.so.%{version} \
  %{buildroot}%{_libdir}/libjbig85.so.%{version}
ln -s libjbig.so.%{version} %{buildroot}%{_libdir}/libjbig.so
ln -s libjbig85.so.%{version} %{buildroot}%{_libdir}/libjbig85.so

install -Dpm0644 libjbig/jbig.h %{buildroot}%{_includedir}/jbig.h
install -Dpm0644 libjbig/jbig85.h %{buildroot}%{_includedir}/jbig85.h
install -Dpm0644 libjbig/jbig_ar.h %{buildroot}%{_includedir}/jbig_ar.h
install -d %{buildroot}%{_bindir} %{buildroot}%{_mandir}/man1
install -pm0755 pbmtools/jbgtopbm pbmtools/jbgtopbm85 \
  pbmtools/pbmtojbg pbmtools/pbmtojbg85 %{buildroot}%{_bindir}/
install -pm0644 pbmtools/jbgtopbm.1 pbmtools/pbmtojbg.1 \
  %{buildroot}%{_mandir}/man1/

%check
LD_LIBRARY_PATH="$PWD/libjbig${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
  %make_build test \
  CC="%{__cc}" \
  CFLAGS="%{optflags} -fPIC -W -Wno-unused-result"

%files
%license COPYING
%{_bindir}/jbgtopbm
%{_bindir}/jbgtopbm85
%{_bindir}/pbmtojbg
%{_bindir}/pbmtojbg85
%{_mandir}/man1/jbgtopbm.1*
%{_mandir}/man1/pbmtojbg.1*

%files libs
%license COPYING
%doc ANNOUNCE CHANGES TODO
%{_libdir}/libjbig.so.%{version}
%{_libdir}/libjbig85.so.%{version}

%files devel
%{_includedir}/jbig.h
%{_includedir}/jbig85.h
%{_includedir}/jbig_ar.h
%{_libdir}/libjbig.so
%{_libdir}/libjbig85.so

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1-1
- Initial openEuler RISC-V package from Fedora 44 and frozen cross-distribution evidence.
