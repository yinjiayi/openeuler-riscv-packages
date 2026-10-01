# SPDX-License-Identifier: Apache-2.0
Name:           perl-Algorithm-LUHN
Version:        1.02
Release:        1%{?dist}
Summary:        Luhn checksum calculation and validation for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Algorithm-LUHN
Source0:        Algorithm-LUHN-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test)
BuildRequires:  perl-generators
Requires:       perl(Exporter)

%description
Algorithm::LUHN calculates check digits and validates identifiers using the
Luhn modulus-10 checksum algorithm.

%prep
%autosetup -n Algorithm-LUHN-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Algorithm/LUHN.pm
%{_mandir}/man3/Algorithm::LUHN.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.02-1
- Package the official CPAN release with all default upstream tests.
