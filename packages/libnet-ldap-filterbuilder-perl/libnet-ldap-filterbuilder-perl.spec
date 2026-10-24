# SPDX-License-Identifier: Apache-2.0
Name:           perl-Net-LDAP-FilterBuilder
Version:        1.200002
Release:        1%{?dist}
Summary:        Build LDAP filter expressions in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Net-LDAP-FilterBuilder
Source0:        Net-LDAP-FilterBuilder-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod >= 1.14
BuildRequires:  perl-Test-Pod-Coverage >= 1.04
BuildRequires:  perl-generators
Requires:       perl(overload)

%description
Net::LDAP::FilterBuilder constructs LDAP filter expressions and supports
composing filters with logical operations.

%prep
%autosetup -n Net-LDAP-FilterBuilder-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Both POD test dependencies are hard requirements, so all four original t/*.t run.
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Net/LDAP/FilterBuilder.pm
%{_mandir}/man3/Net::LDAP::FilterBuilder.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.200002-1
- Package publisher-verified CPAN release with all original default tests.
