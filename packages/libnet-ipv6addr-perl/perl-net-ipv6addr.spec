# SPDX-License-Identifier: Apache-2.0
Name:           perl-net-ipv6addr
Version:        1.02
Release:        1%{?dist}
Summary:        Parse and format IPv6 addresses in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Net-IPv6Addr
Source0:        Net-IPv6Addr-1.02.tar.gz
Source1:        Regexp-IPv6-0.03.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Math::BigInt) >= 1.999813
BuildRequires:  perl(Math::BigInt::Calc)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  findutils
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(Test)
BuildRequires:  perl(utf8)
BuildRequires:  tar
BuildRequires:  gzip
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(Exporter)
Requires:       perl(Math::BigInt) >= 1.999813
Requires:       perl(Math::BigInt::Calc)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Net::IPv6Addr parses, validates and formats IPv6 addresses, including
conversion to and from large integers.

%prep
%autosetup -n Net-IPv6Addr-%{version} -p1
# Retain the original grant and the complete notice for copied code/tests.
%{__perl} -0777 -ne 'print $1 if /(^=head1 LICENSE\n.*\z)/ms' \
    lib/Net/IPv6Addr.pod > LICENSE
tar -xOzf "%{SOURCE1}" Regexp-IPv6-0.03/README > NOTICE.Regexp-IPv6
test -s LICENSE && test -s NOTICE.Regexp-IPv6

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE NOTICE.Regexp-IPv6
%doc README Changes
%{perl_vendorlib}/Net/IPv6Addr.pm
%{perl_vendorlib}/Net/IPv6Addr.pod
%{_mandir}/man3/Net::IPv6Addr.3*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.02-1
- Package Net::IPv6Addr with original tests and full source notices.
