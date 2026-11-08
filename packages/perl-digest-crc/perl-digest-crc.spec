# SPDX-License-Identifier: Apache-2.0
Name:           perl-digest-crc
Version:        0.24
Release:        1%{?dist}
Summary:        Compute cyclic redundancy checks in Perl with XS acceleration
License:        LicenseRef-Public-Domain AND Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Digest-CRC
Source0:        Digest-CRC-%{version}.tar.gz
Patch0:         0001-preserve-source-license-notices.patch
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl(B)
BuildRequires:  perl-generators
Requires:       perl
Requires:       perl(B)

%description
Digest::CRC computes configurable cyclic redundancy checks, including CRC-32
and CRC-64, through functional and incremental Perl interfaces. A CRC detects
accidental data corruption; it does not provide cryptographic integrity.

%prep
%setup -q -n Digest-CRC-%{version}
%global _default_patch_fuzz 0
%patch -P 0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build OPTIMIZE="%{optflags}"

%install
make pure_install DESTDIR=%{buildroot}
test -s %{buildroot}%{perl_vendorarch}/auto/Digest/CRC/CRC.so

%check
%{__perl} -Mblib -MDigest::CRC -MB -e 'die "Digest::CRC XS not loaded" unless B::svref_2object(\&Digest::CRC::_crc)->XSUB'
make test
WITH_CRC64=1 make test

%files
%license README COPYING.Artistic1 NOTICE.Scope
%doc Changes
%{perl_vendorarch}/Digest/CRC.pm
%{perl_vendorarch}/auto/Digest/CRC/
%{_mandir}/man3/Digest::CRC.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.24-1
- Import the exact release with unchanged default tests and real XS validation.
