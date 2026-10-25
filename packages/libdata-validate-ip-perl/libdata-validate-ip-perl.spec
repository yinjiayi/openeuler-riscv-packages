# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Data-Validate-IP
Version:        0.31
Release:        1%{?dist}
Summary:        Validate IPv4 and IPv6 addresses and network membership
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Validate-IP
Source0:        Data-Validate-IP-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(NetAddr::IP) >= 4
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Test::Requires)
# t/Untaint.t otherwise silently skips its taint assertions.
BuildRequires:  perl(Test::Taint)
BuildRequires:  perl-generators

%description
Data::Validate::IP validates IPv4 and IPv6 address strings and tests
membership in address ranges. The module provides both Socket-backed and
pure-Perl validation paths.

%prep
%autosetup -n Data-Validate-IP-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all four default upstream files, including slow and taint tests.
%make_build test

%files
%license LICENSE
%doc Changes README.md
%{perl_vendorlib}/Data/Validate/IP.pm
%{_mandir}/man3/Data::Validate::IP.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.31-1
- Package the official CPAN release with its unchanged default test suite.
