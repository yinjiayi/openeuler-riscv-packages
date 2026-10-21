# SPDX-License-Identifier: Apache-2.0
Name:           perl-MIME-tools
Version:        5.519
Release:        1%{?dist}
Summary:        Perl modules for MIME-compliant messages
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/MIME-tools
Source0:        MIME-tools-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gzip
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Deep
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
BuildRequires:  perl(Convert::BinHex)
BuildRequires:  perl(MIME::Base64) >= 2.20
BuildRequires:  perl(Mail::Field) >= 1.05
BuildRequires:  perl(Mail::Header) >= 1.09
BuildRequires:  perl(Mail::Internet) >= 1.28
Requires:       gzip
Requires:       perl(Convert::BinHex)
Requires:       perl(MIME::Base64) >= 2.20
Requires:       perl(Mail::Field) >= 1.05
Requires:       perl(Mail::Header) >= 1.09
Requires:       perl(Mail::Internet) >= 1.28

%description
MIME-tools provides Perl modules to parse, create, and decode MIME messages.
It supplies MIME::Parser and MIME::Entity required by ytnefprocess.

%prep
%autosetup -n MIME-tools-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run every upstream default test, including the 5.519 concatenated-base64
# regression, the localhost SMTP exchange, and the gzip/BinHex decoder cases.
# Upstream author-only Kwalitee and opt-in POD coverage remain conditional.
%make_build test

%files
%license COPYING
%doc ChangeLog README examples
%{perl_vendorlib}/MIME/
%{_mandir}/man3/MIME*.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.519-1
- Package the official CPAN release and full default upstream test suite.
