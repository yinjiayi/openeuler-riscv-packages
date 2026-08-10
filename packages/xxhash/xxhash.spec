# SPDX-License-Identifier: Apache-2.0
Name:           xxhash
Version:        0.8.3
Release:        1%{?dist}
Summary:        Extremely fast non-cryptographic hash algorithm
License:        BSD-2-Clause AND GPL-2.0-or-later
URL:            https://github.com/Cyan4973/xxHash
Source0:        xxhash-0.8.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make


%description
xxHash provides a very fast non-cryptographic hash library and command-line
checksum utility.

%package devel
Summary:        Development files for xxHash
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, static library, and pkg-config metadata for xxHash.

%prep
%autosetup -p1 -n xxHash-%{version}

%build
# The upstream Makefile defaults to -O3 and otherwise drops the distribution
# hardening and debug flags.  Keep these in the environment rather than on the
# make command line so the shared-library target can append its required
# -shared linker flag.
export CFLAGS="%{optflags}"
export LDFLAGS="%{__global_ldflags}"
%make_build

%install
%make_install \
  PREFIX=%{_prefix} \
  LIBDIR=%{_libdir} \
  MANDIR=%{_mandir}/man1

%check
export CFLAGS="%{optflags}"
export LDFLAGS="%{__global_ldflags}"
%make_build check

%files
%license LICENSE cli/COPYING
%doc README.md
%{_bindir}/xxh*sum
%{_libdir}/libxxhash.so.0*
%{_mandir}/man1/xxh*sum.1*

%files devel
%license LICENSE
%{_includedir}/xxh3.h
%{_includedir}/xxhash.h
%{_libdir}/libxxhash.a
%{_libdir}/libxxhash.so
%{_libdir}/pkgconfig/libxxhash.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.8.3-1
- Initial openEuler RISC-V package.
