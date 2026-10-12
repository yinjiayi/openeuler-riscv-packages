# SPDX-License-Identifier: Apache-2.0
Name:           perl-Test-Identity
Version:        0.01
Release:        1%{?dist}
Summary:        Assert Perl reference identity
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Test-Identity
Source0:        Test-Identity-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::Builder::Module)
BuildRequires:  perl(Test::Builder::Tester)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl-generators
Requires:       perl(Scalar::Util)
Requires:       perl(Test::Builder::Module)

%description
Test::Identity checks whether two Perl values refer to exactly the same
reference, including values whose stringification is overloaded.

%prep
%autosetup -n Test-Identity-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all three original default files, including the POD check.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Test/Identity.pm
%{_mandir}/man3/Test::Identity.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.01-1
- Package official CPAN release with all default tests.
