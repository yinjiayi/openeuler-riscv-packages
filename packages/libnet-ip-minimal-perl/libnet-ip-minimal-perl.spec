# SPDX-License-Identifier: Apache-2.0
Name:           perl-Net-IP-Minimal
Version:        0.06
Release:        1%{?dist}
Summary:        Minimal IPv4 and IPv6 classification functions for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Net-IP-Minimal
Source0:        Net-IP-Minimal-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Exporter)

%description
Net::IP::Minimal exports small functions to classify IPv4 and IPv6 address
strings and report their IP version. It performs no network operations.

%prep
%autosetup -n Net-IP-Minimal-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all four original tests; upstream skips two release-only files.
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Net/IP/Minimal.pm
%{_mandir}/man3/Net::IP::Minimal.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.06-1
- Package official CPAN release with unchanged default upstream tests.
