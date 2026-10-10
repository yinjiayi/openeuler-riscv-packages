# SPDX-License-Identifier: Apache-2.0
Name:           perl-Net-DNS-Resolver-Mock
Version:        1.20230216
Release:        1%{?dist}
Summary:        Mock Net::DNS resolver backed by local zone data
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Net-DNS-Resolver-Mock
Source0:        Net-DNS-Resolver-Mock-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Net-DNS
BuildRequires:  perl-Test-Exception
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Net::DNS::Packet)
Requires:       perl(Net::DNS::Question)
Requires:       perl(Net::DNS::Resolver)
Requires:       perl(Net::DNS::ZoneFile)

%description
Net::DNS::Resolver::Mock uses local zone data to answer DNS lookup calls
without sending them to an external resolver.

%prep
%autosetup -n Net-DNS-Resolver-Mock-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# All five original t/*.t remain present. The two author-only files skip
# themselves unless upstream's AUTHOR_TESTING is explicitly enabled.
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Net/DNS/Resolver/Mock.pm
%{_mandir}/man3/Net::DNS::Resolver::Mock.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.20230216-1
- Package publisher-verified CPAN source with unchanged default tests.
