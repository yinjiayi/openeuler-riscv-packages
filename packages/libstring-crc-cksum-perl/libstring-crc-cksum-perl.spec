# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-CRC-Cksum
Version:        0.91
Release:        1%{?dist}
Summary:        Compute POSIX cksum-compatible CRC values from Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-CRC-Cksum
Source0:        String-CRC-Cksum-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
BuildRequires:  coreutils

%description
String::CRC::Cksum computes 32-bit CRC and size values compatible with
the POSIX cksum command for strings and filehandles.

%prep
%autosetup -n String-CRC-Cksum-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# The complete upstream suite includes an optional /etc/profile comparison
# with /usr/bin/cksum; retain its original conditional-skip behavior.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/String/CRC/Cksum.pm
%{_mandir}/man3/String::CRC::Cksum.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.91-1
- Package official CPAN release with complete default upstream test suite.
