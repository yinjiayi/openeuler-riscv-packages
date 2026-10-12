# SPDX-License-Identifier: Apache-2.0
Name:           libcidr
Version:        1.2.3
Release:        1%{?dist}
Summary:        IPv4 and IPv6 CIDR address manipulation library
License:        BSD-2-Clause AND BSD-4-Clause-UC
URL:            https://www.over-yonder.net/~fullermd/projects/libcidr
Source0:        libcidr-%{version}.tar.xz
Patch0:         0001-regression-report-failures.patch

BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-interpreter

%description
LibCIDR parses and manipulates IPv4 and IPv6 addresses and CIDR blocks. The
package includes the cidrcalc command-line utility.

%package devel
Summary:        Development files for libcidr
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The public C header, unversioned library link, documentation, and examples
for applications using libcidr.

%prep
%autosetup -p1

%build
%make_build \
  PREFIX=%{_prefix} \
  CIDR_LIBDIR=%{_libdir} \
  CIDR_MANDIR=%{_mandir} \
  CIDR_DOCDIR=%{_docdir}/%{name}-devel/docs \
  CIDR_EXDIR=%{_docdir}/%{name}-devel/examples

%install
%make_install \
  PREFIX=%{_prefix} \
  CIDR_LIBDIR=%{_libdir} \
  CIDR_MANDIR=%{_mandir} \
  CIDR_DOCDIR=%{_docdir}/%{name}-devel/docs \
  CIDR_EXDIR=%{_docdir}/%{name}-devel/examples

%check
# Build all seven upstream test programs and execute the complete registered
# regression data set. The package patch makes any reported failure fatal.
for program in compare inaddr kids mkstr netbc nums parent; do
  %{__make} -C src/test/${program} all
done
(cd src/test/regression && perl -I . ./test.pl)

%files
%license LICENSE
%doc README
%{_bindir}/cidrcalc
%{_libdir}/libcidr.so.0
%{_mandir}/man3/libcidr.3*

%files devel
%license LICENSE
%{_includedir}/libcidr.h
%{_libdir}/libcidr.so
%{_docdir}/%{name}-devel/

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.3-1
- Package official libcidr with fail-closed full upstream regression tests.
