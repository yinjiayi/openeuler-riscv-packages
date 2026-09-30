# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Context-EitherSide
Version:        1.4
Release:        1%{?dist}
Summary:        Extract words around search terms in Perl text
License:        Artistic-2.0
URL:            https://metacpan.org/dist/Text-Context-EitherSide
Source0:        Text-Context-EitherSide-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-generators

%description
Text::Context::EitherSide returns a short context around one or more search
terms in a string.

%prep
%autosetup -n Text-Context-EitherSide-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain the functional, POD and POD-coverage tests. Build requirements make
# the two optional POD suites mandatory in the target build environment.
%make_build test

%files
%doc README Changes
%{perl_vendorlib}/Text/Context/EitherSide.pm
%{_mandir}/man3/Text::Context::EitherSide.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4-1
- Package the official CPAN release with all default upstream tests.
