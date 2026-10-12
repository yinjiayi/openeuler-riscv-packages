# SPDX-License-Identifier: Apache-2.0

Name:           ffcall
Version:        2.5
Release:        1%{?dist}
Summary:        Libraries for foreign function call interfaces
License:        GPL-2.0-or-later AND LGPL-2.1-or-later
URL:            https://www.gnu.org/software/libffcall/
Source0:        libffcall-%{version}.tar.gz

BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  grep
BuildRequires:  make
Provides:       bundled(gnulib)

%description
GNU libffcall provides libraries for building foreign function call
interfaces in embedded interpreters. It supports dynamically assembled calls,
callbacks, reentrant variable-argument receivers, and executable trampolines.

%package devel
Summary:        Development files for GNU libffcall
License:        GPL-2.0-or-later AND LGPL-2.1-or-later AND (GPL-2.0-or-later OR GFDL-1.2-no-invariants-or-later)
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, unversioned linker names, and manuals for developing applications
with GNU libffcall.

%package static
Summary:        Static libraries for GNU libffcall
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static libraries for applications that require static GNU libffcall linkage.

%prep
%autosetup -n libffcall-%{version} -p1

%build
# Upstream's RISC-V assembly templates contain PIC and non-PIC branches. Use
# the PIC branch so libvacall.a remains compatible with hardened PIE consumers.
export CPP="%{__cc} -E -fPIC"
%configure
# Upstream explicitly declares that its build does not support parallel make.
%make_build -j1 CPP="$CPP"

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_datadir}/html
# Upstream installs versioned shared objects without execute bits. Mark them as
# shared libraries so RPM's find-debuginfo pass discovers their DWARF sections.
chmod a+x %{buildroot}%{_libdir}/lib*.so.*

%check
# Keep the complete C and C++ suite under openEuler's PIE hardening. The CPP
# override selects the PIC RISC-V assembly branch used by static libvacall.
make -j1 \
  CPP="%{__cc} -E -fPIC" \
  CFLAGS="%{build_cflags} -fPIE" \
  CXXFLAGS="%{build_cxxflags} -fPIE" \
  LDFLAGS="%{build_ldflags} -pie" \
  check

%files
%license COPYING
%doc NEWS README
%{_libdir}/libavcall.so.1*
%{_libdir}/libcallback.so.1*
%{_libdir}/libffcall.so.0*
%{_libdir}/libtrampoline.so.1*

%files devel
%{_includedir}/avcall.h
%{_includedir}/callback.h
%{_includedir}/ffcall-abi.h
%{_includedir}/ffcall-version.h
%{_includedir}/trampoline.h
%{_includedir}/vacall.h
%{_includedir}/vacall_r.h
%{_libdir}/libavcall.so
%{_libdir}/libcallback.so
%{_libdir}/libffcall.so
%{_libdir}/libtrampoline.so
%{_mandir}/man3/avcall.3*
%{_mandir}/man3/callback.3*
%{_mandir}/man3/trampoline.3*
%{_mandir}/man3/vacall.3*

%files static
%{_libdir}/*.a

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.5-1
- Initial openEuler RISC-V package with the complete upstream C and C++ suite.
- Select upstream's PIC RISC-V assembly and retain PIE hardening in the suite.
- Package all static archives separately from headers and shared-library links.
- Mark shared objects executable so RPM emits non-empty debuginfo artifacts.
