# SPDX-License-Identifier: Apache-2.0

Name:           adns
Version:        1.6.2
Release:        1%{?dist}
Summary:        Asynchronous-capable DNS resolver library and utilities
License:        GPL-3.0-or-later
URL:            https://www.chiark.greenend.org.uk/~ian/adns/
Source0:        adns-%{version}.tar.gz

BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  gcc
BuildRequires:  grep
BuildRequires:  m4
BuildRequires:  make
BuildRequires:  sed

%description
adns is an asynchronous-capable DNS resolver library with synchronous and
asynchronous interfaces plus command-line query and log-processing tools.

%package devel
Summary:        Development files for adns
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header, linker name, and static library for developing applications with adns.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
# Upstream applies DESTDIR twice in its recursive install rules. Pass absolute
# staged directories with an empty DESTDIR so every file is installed once.
make install \
  DESTDIR= \
  prefix=%{buildroot}%{_prefix} \
  exec_prefix=%{buildroot}%{_exec_prefix} \
  bindir=%{buildroot}%{_bindir} \
  libdir=%{buildroot}%{_libdir} \
  includedir=%{buildroot}%{_includedir}

%check
make check

%files
%license COPYING
%doc NEWS README README.html changelog
%{_bindir}/adnsheloex
%{_bindir}/adnshost
%{_bindir}/adnslogres
%{_bindir}/adnsresfilter
%{_libdir}/libadns.so.1*

%files devel
%{_includedir}/adns.h
%{_libdir}/libadns.a
%{_libdir}/libadns.so

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.2-1
- Initial openEuler RISC-V package with the complete upstream regression suite.
