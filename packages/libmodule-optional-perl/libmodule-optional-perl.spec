# SPDX-License-Identifier: Apache-2.0
Name:           perl-Module-Optional
Version:        0.03
Release:        1%{?dist}
Summary:        Optional Perl module loading with fallback implementations
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Module-Optional
Source0:        Module-Optional-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple >= 0.44
BuildRequires:  perl-generators
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.00
Requires:       perl(Test::Simple) >= 0.44

%description
Module::Optional loads an optional Perl module when available and otherwise
uses its accompanying fallback module. The distribution also provides
Params::Validate::Dummy as a fallback implementation.

%prep
%autosetup -n Module-Optional-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep every upstream default test, including the POD and coverage files.
%make_build test

%files
%license LICENSE
%doc Changes README Todo
%{perl_vendorlib}/Module/Optional.pm
%{perl_vendorlib}/Params/Validate/Dummy.pm
%{_mandir}/man3/Module::Optional.3*
%{_mandir}/man3/Params::Validate::Dummy.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.03-1
- Package the official CPAN release with the full upstream default test suite.
