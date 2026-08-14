# SPDX-License-Identifier: Apache-2.0
Name:           libdill
Version:        2.14
Release:        1%{?dist}
Summary:        Structured concurrency library for C
License:        MIT
URL:            https://github.com/sustrik/libdill
Source0:        libdill-%{version}.tar.gz
Patch0:         0001-fix-compilation-for-gcc-9.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
libdill is a C library that provides structured concurrency primitives,
coroutines, channels, and nonblocking socket interfaces.

%package devel
Summary:        Development files for libdill
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, the unversioned linker name, pkg-config metadata, and API manual
pages for developing applications with libdill.

%prep
%autosetup -p1
# The release archive has no .git directory. Supply the version consumed by
# package_version.sh before regenerating the Autotools files.
printf '%s\n' '%{version}' > .version

%build
./autogen.sh
%configure --enable-shared --disable-static
# The upstream fallback stack switch documents that stack protector is not
# compatible with non-x86 coroutine stacks.
%make_build CFLAGS="%{optflags} -fno-stack-protector"

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la

%check
# Keep the complete upstream test suite enabled; serialize socket tests so
# parallel jobs do not share temporary endpoints.
%make_build -j1 check

%files
%license COPYING
%doc AUTHORS README.md
%{_libdir}/libdill.so.*

%files devel
%license COPYING
%{_includedir}/libdill.h
%{_includedir}/libdillimpl.h
%{_libdir}/libdill.so
%{_libdir}/pkgconfig/libdill.pc
%{_mandir}/man3/*.3*

%changelog
* Fri Aug 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.14-1
- Initial openEuler RISC-V package from the independently verified upstream tag.
- Apply the post-release upstream fix for GCC 9 and newer.
