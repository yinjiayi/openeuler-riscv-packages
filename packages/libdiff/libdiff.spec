# SPDX-License-Identifier: Apache-2.0
Name:           libdiff
Version:        0.1.0
Release:        1%{?dist}
Summary:        Shortest edit script and sequence difference library
License:        MIT AND BSD-3-Clause AND ISC
URL:            https://github.com/kristapsdz/libdiff
Source0:        libdiff-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
Libdiff computes shortest edit scripts, longest common subsequences and
edit distances for arbitrary byte sequences. This package contains its
character and word difference command-line examples.

%package devel
Summary:        Header and static library for libdiff consumers
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Public header, static library and API manual for libdiff development.

%prep
%autosetup -n libdiff-VERSION_0_1_0 -p1

%build
CFLAGS="%{build_cflags}" ./configure PREFIX=%{_prefix} \
  LIBDIR=%{_libdir} INCLUDEDIR=%{_includedir} MANDIR=%{_mandir} \
  LDFLAGS="%{build_ldflags}"
%make_build

%install
%make_install
install -D -m 0755 diffchars %{buildroot}%{_bindir}/diffchars
install -D -m 0755 diffwords %{buildroot}%{_bindir}/diffwords

%check
# Upstream tests.c contains configure probes, not a registered runtime suite.
# Exercise both programs against known one-replacement differences.
./diffchars abc adc | grep -Fx 'Edit distance: 2'
./diffwords 'alpha beta' 'alpha gamma' | grep -Fx 'Edit distance: 2'

%files
%license LICENSE.md
%doc README.md
%{_bindir}/diffchars
%{_bindir}/diffwords

%files devel
%license LICENSE.md
%{_includedir}/diff.h
%{_libdir}/libdiff.a
%{_mandir}/man3/diff.3*

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.0-1
- Package the official libdiff 0.1.0 release with functional checks.
