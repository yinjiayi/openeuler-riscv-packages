# SPDX-License-Identifier: Apache-2.0
Name:           libtomcrypt
Version:        1.18.2
Release:        1%{?dist}
Summary:        Portable modular cryptographic toolkit
License:        LicenseRef-Public-Domain OR WTFPL
URL:            https://www.libtom.net/LibTomCrypt/
Source0:        crypt-1.18.2.tar.xz
Patch0:         0001-fix-CVE-2019-17362.patch
Patch1:         0002-fix-missing-mutex-unlock.patch
Patch2:         0003-fix-CCM-bounds-and-warning.patch

BuildRequires:  gcc
BuildRequires:  libtommath-devel
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
Portable modular cryptographic toolkit with symmetric and public-key
algorithms, hashes, MACs, and password-based cryptography.

%package devel
Summary:        Development files for libtomcrypt
Requires:       libtomcrypt%{?_isa} = %{version}-%{release}

%description devel
Headers, shared-library links, and pkg-config metadata for libtomcrypt.

%prep
%autosetup -p1

%build
%set_build_flags
export PREFIX="%{_prefix}"
export INCPATH="%{_includedir}"
export LIBPATH="%{_libdir}"
export EXTRALIBS="-ltommath"
export CFLAGS="%{build_cflags} -DLTM_DESC -DUSE_LTM"
%make_build -f makefile.shared library

%install
%make_install -f makefile.shared INSTALL_OPTS="-m 755" \
  INCPATH="%{_includedir}" LIBPATH="%{_libdir}"
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete
sed -i \
  -e 's|^prefix=.*|prefix=%{_prefix}|g' \
  -e 's|^libdir=.*|libdir=${prefix}/%{_lib}|g' \
  %{buildroot}%{_libdir}/pkgconfig/libtomcrypt.pc

%check
%make_build -f makefile.shared test
./test

%ldconfig_scriptlets

%files
%license LICENSE
%doc README.md
%{_libdir}/libtomcrypt.so.*

%files devel
%{_includedir}/*.h
%{_libdir}/libtomcrypt.so
%{_libdir}/pkgconfig/libtomcrypt.pc

%changelog
* Sun Aug 16 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.18.2-1
- Package the upstream library, full self-test suite, and accepted upstream fixes.
