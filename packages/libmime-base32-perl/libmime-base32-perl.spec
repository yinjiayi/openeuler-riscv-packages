# SPDX-License-Identifier: Apache-2.0
Name:           perl-MIME-Base32
Version:        1.303
Release:        1%{?dist}
Summary:        Base32 and base32hex encoding and decoding for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/MIME-Base32
Source0:        MIME-Base32-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
MIME::Base32 encodes and decodes binary data using Base32 or base32hex.

%prep
%autosetup -n MIME-Base32-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Makefile.PL selects t/*.t and xt/*.t; this release has two t files and no xt files.
%make_build test

%files
%license LICENSE ARTISTIC-1.0 GPL-1
%doc Changes README.md
%{perl_vendorlib}/MIME/Base32.pm
%{_mandir}/man3/MIME::Base32.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.303-1
- Package the official CPAN release and retain the complete default test suite.
