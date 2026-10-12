# SPDX-License-Identifier: Apache-2.0
Name:           perl-Net-CIDR-Set
Version:        0.23
Release:        1%{?dist}
Summary:        IPv4 and IPv6 address-set operations for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Net-CIDR-Set
Source0:        Net-CIDR-Set-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Module-Metadata
BuildRequires:  perl-Data-Dumper
BuildRequires:  perl-Test-Exception
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-namespace-autoclean
BuildRequires:  perl-generators
Requires:       perl(namespace::autoclean) >= 0.29

%description
Net::CIDR::Set implements IPv4 and IPv6 address sets with CIDR and range
parsing, union, intersection, subtraction, and iteration.

%prep
%autosetup -n Net-CIDR-Set-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all ten default upstream test files, including prerequisite reporting.
%make_build test

%files
%license LICENSE
%doc Changes README.md
%{perl_vendorlib}/Net/CIDR/Set.pm
%{perl_vendorlib}/Net/CIDR/Set/
%{_mandir}/man3/Net::CIDR::Set*.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.23-1
- Package the official CPAN release with unchanged default upstream tests.
