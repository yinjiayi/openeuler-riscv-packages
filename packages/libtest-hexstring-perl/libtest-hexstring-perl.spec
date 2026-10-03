# SPDX-License-Identifier: Apache-2.0
Name:           perl-Test-HexString
Version:        0.03
Release:        1%{?dist}
Summary:        Compare Perl strings with hexadecimal diagnostics
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Test-HexString
Source0:        Test-HexString-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::Builder::Module)
BuildRequires:  perl(Test::Builder::Tester)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl-generators
Requires:       perl(Test::Builder)
Requires:       perl(Test::Builder::Module)

%description
Test::HexString compares strings and prints a hexadecimal dump around
differences, making binary-string test failures easier to diagnose.

%prep
%autosetup -n Test-HexString-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all three original default files, including binary diagnostics
# and the POD check.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Test/HexString.pm
%{_mandir}/man3/Test::HexString.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.03-1
- Package official CPAN release with all default tests.
