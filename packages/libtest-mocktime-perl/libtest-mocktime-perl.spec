# SPDX-License-Identifier: Apache-2.0
Name:           perl-Test-MockTime
Version:        0.17
Release:        1%{?dist}
Summary:        Mock Perl time functions for deterministic tests
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Test-MockTime
Source0:        Test-MockTime-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl(Time::Piece) >= 1.08
BuildRequires:  perl-generators

%description
Test::MockTime overrides Perl's time, localtime and gmtime functions so
tests can observe a selected or fixed time.

%prep
%autosetup -n Test-MockTime-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all five default upstream tests, including the optional POD test.
%make_build test

%files
%doc README Changes
%{perl_vendorlib}/Test/MockTime.pm
%{_mandir}/man3/Test::MockTime.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.17-1
- Package official CPAN release with the complete default test suite.
