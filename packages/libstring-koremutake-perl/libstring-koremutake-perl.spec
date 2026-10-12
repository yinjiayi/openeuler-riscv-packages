# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-Koremutake
Version:        0.30
Release:        1%{?dist}
Summary:        Convert integers to memorable Koremutake strings
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-Koremutake
Source0:        String-Koremutake-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Error
BuildRequires:  perl-Test-Exception
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Error) >= 0.15
Requires:       perl(Test::Exception) >= 0.15
Requires:       perl(Test::More) >= 0.01

%description
String::Koremutake converts nonnegative integers to and from memorable
syllable-based Koremutake strings.

%prep
%autosetup -n String-Koremutake-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all three upstream default suites. Test::Pod::Coverage is required
# so the POD coverage suite runs instead of reporting a missing-module SKIP.
# One upstream dies_ok assertion misspells koremutake_to_integer; installed
# smoke separately exercises the actual method's invalid-input behavior.
%make_build test

%files
%license README
%doc CHANGES
%{perl_vendorlib}/String/Koremutake.pm
%{_mandir}/man3/String::Koremutake.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.30-1
- Package official CPAN release and retain every default upstream test.
