# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-Interpolate-Named
Version:        1.06
Release:        1%{?dist}
Summary:        Interpolate named values into Perl strings
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-Interpolate-Named
Source0:        String-Interpolate-Named-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
String::Interpolate::Named substitutes named variables in strings and also
supports conditional choices and indexed values.

%prep
%autosetup -n String-Interpolate-Named-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all eight upstream default suites and their included data fixtures.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/String/Interpolate/Named.pm
%{_mandir}/man3/String::Interpolate::Named.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.06-1
- Package official CPAN release with all default upstream tests.
