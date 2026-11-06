# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Math-VecStat
Version:        0.08
Release:        1%{?dist}
Summary:        Basic vector statistics functions for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Math-VecStat
Source0:        Math-VecStat-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators

%description
Math::VecStat provides minimum, maximum, average, median and other vector
operations for Perl.

%prep
%autosetup -n Math-VecStat-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain the original t/VecStat.t and all 40 assertions.
%make_build test

%files
%license README
%{perl_vendorlib}/Math/VecStat.pm
%{_mandir}/man3/Math::VecStat.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.08-1
- Package official CPAN release with complete default test.
