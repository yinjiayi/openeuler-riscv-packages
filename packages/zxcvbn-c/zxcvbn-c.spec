# SPDX-License-Identifier: Apache-2.0
Name:           zxcvbn-c
Version:        2.6
Release:        1%{?dist}
Summary:        C and C++ password strength estimator
License:        MIT
URL:            https://github.com/tsyrogit/zxcvbn-c
Source0:        zxcvbn-c-2.6.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
zxcvbn-c estimates password strength using common words, names, and patterns.

%package devel
Summary:        Development files for zxcvbn-c
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header and libraries for developing applications with zxcvbn-c.

%prep
%autosetup -p1

%build
%make_build all \
  CC=%{__cc} \
  CXX=%{__cxx} \
  CFLAGS='%{optflags} -Wall -Wextra' \
  CXXFLAGS='%{optflags} -Wall -Wextra' \
  LDFLAGS='%{__global_ldflags}'

%install
%make_install \
  PREFIX=%{_prefix} \
  LIBDIR=%{_libdir} \
  BINDIR=%{_bindir} \
  INCLUDEDIR=%{_includedir}/zxcvbn \
  DATADIR=%{_datadir}

%check
%make_build test

%files
%license LICENSE.txt
%doc README.md
%{_bindir}/zxcvbn-dictgen
%{_libdir}/libzxcvbn.so.0*
%{_datadir}/zxcvbn/

%files devel
%license LICENSE.txt
%{_includedir}/zxcvbn/
%{_libdir}/libzxcvbn.so
%{_libdir}/libzxcvbn.a

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.6-1
- Initial openEuler RISC-V package.

