# SPDX-License-Identifier: Apache-2.0
Name:           perl-Test-ClassAPI
Version:        1.07
Release:        1%{?dist}
Summary:        First-pass API tests for Perl class hierarchies
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Test-ClassAPI
Source0:        Test-ClassAPI-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Class::Inspector) >= 1.12
BuildRequires:  perl(Config::Tiny) >= 2.00
BuildRequires:  perl(Params::Util) >= 1.00
BuildRequires:  perl(File::Spec) >= 0.83
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Class::Inspector) >= 1.12
Requires:       perl(Config::Tiny) >= 2.00
Requires:       perl(Params::Util) >= 1.00
Requires:       perl(File::Spec) >= 0.83
Requires:       perl(Test::More) >= 0.47

%description
Test::ClassAPI checks declared class methods, inheritance and interface
requirements as a first-pass API test for Perl class hierarchies.

%prep
%autosetup -n Test-ClassAPI-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all five default upstream tests without suppression.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Test/ClassAPI.pm
%{_mandir}/man3/Test::ClassAPI.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.07-1
- Package official CPAN release with unchanged upstream default tests.
