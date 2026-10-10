# SPDX-License-Identifier: Apache-2.0
Name:           perl-Net-DHCPv6-DUID-Parser
Version:        1.01
Release:        1%{?dist}
Summary:        Parse DHCPv6 unique identifiers in Perl
License:        BSD-2-Clause-Views
URL:            https://metacpan.org/dist/Net-DHCPv6-DUID-Parser
Source0:        Net-DHCPv6-DUID-Parser-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Carp)

%description
Net::DHCPv6::DUID::Parser decodes DHCPv6 unique identifiers into their type,
hardware, enterprise, link-address, and timestamp fields.

%prep
%autosetup -n Net-DHCPv6-DUID-Parser-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve the sole unchanged upstream test and all 46 default assertions.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Net/DHCPv6/DUID/Parser.pm
%{_mandir}/man3/Net::DHCPv6::DUID::Parser.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.01-1
- Package official CPAN release with its unchanged default upstream test.
