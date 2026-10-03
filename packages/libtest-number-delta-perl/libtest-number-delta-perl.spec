# SPDX-License-Identifier: Apache-2.0
Name:           perl-Test-Number-Delta
Version:        1.06
Release:        1%{?dist}
Summary:        Compare numbers within a specified tolerance in Perl tests
License:        Apache-2.0
URL:            https://metacpan.org/dist/Test-Number-Delta
Source0:        Test-Number-Delta-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Test::Builder)

%description
Test::Number::Delta checks whether numeric values differ by no more than
a specified absolute or relative tolerance.

%prep
%autosetup -n Test-Number-Delta-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all 12 default upstream test files, including Test::Builder integration.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Test/Number/Delta.pm
%{_mandir}/man3/Test::Number::Delta.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.06-1
- Package official CPAN release with all default upstream tests.
