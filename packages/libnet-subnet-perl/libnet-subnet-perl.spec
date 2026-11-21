# SPDX-License-Identifier: Apache-2.0
Name:           libnet-subnet-perl
Version:        1.03
Release:        1%{?dist}
Summary:        Match and classify IPv4 and IPv6 addresses by subnet in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Net-Subnet
Source0:        Net-Subnet-1.03.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Socket6) >= 0.23
BuildRequires:  perl(Exporter)
BuildRequires:  perl(base)
BuildRequires:  perl(strict)
BuildRequires:  perl(constant)
BuildRequires:  perl(Test::More)
Requires:       perl
Requires:       perl(Socket)
Requires:       perl(Socket6) >= 0.23
Requires:       perl(Exporter)
Requires:       perl(base)
Requires:       perl(strict)
Requires:       perl(constant)

%description
Match and classify IPv4 and IPv6 addresses using CIDR prefixes or subnet
masks. Classifiers can prefer more-specific prefixes.

%prep
%autosetup -n Net-Subnet-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .
cat <<'UPSTREAM_NOTICE' > Net-Subnet-NOTICE
Net::Subnet, Juerd Waalboer <juerd@cpan.org>.
The original Perl dual grant remains in lib/Net/Subnet.pm:
This library is free software; you can redistribute it and/or modify it under
the same terms as Perl itself.
UPSTREAM_NOTICE

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
make test TEST_VERBOSE=1

%files
%license Net-Subnet-NOTICE Artistic-1.0-Perl.txt GPL-1.0.txt
%doc README Changes
%{perl_vendorlib}/Net/Subnet.pm
%{_mandir}/man3/Net::Subnet.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.03-1
- Package the signed official release and preserve both original test files.
