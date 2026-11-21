# SPDX-License-Identifier: Apache-2.0
Name:           perl-Convert-Base32
Version:        0.06
Release:        1%{?dist}
Summary:        Encode and decode Base32 strings in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Convert-Base32
Source0:        Convert-Base32-0.06.tar.gz
Patch0:         0001-encode-large-input-tail-bits.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Carp
BuildRequires:  perl-Exporter
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Exception
BuildRequires:  perl-generators

%description
Convert::Base32 encodes and decodes the unpadded Base32 strings described by
the RACE internet draft, with lowercase output and case-insensitive decoding.

%prep
%autosetup -n Convert-Base32-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%make_build test

%files
%license README lib/Convert/Base32.pm
%doc Changes
%{perl_vendorlib}/Convert/Base32.pm
%{_mandir}/man3/Convert::Base32.3*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.06-1
- Package the official release; fix large-input tail bits with added regressions.
