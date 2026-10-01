# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Header
Version:        1.03
Release:        1%{?dist}
Summary:        Perl helpers for constructing and parsing text headers
License:        GPL-2.0-or-later
URL:            https://metacpan.org/dist/Text-Header
Source0:        Text-Header-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators

%description
Text::Header provides header and unheader functions for constructing and
parsing generic RFC 822-style text header lines. It does not provide HTTP
specific defaults or validation of untrusted header content.

%prep
%autosetup -n Text-Header-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep the sole unmodified upstream default test.pl load assertion.
%make_build test

%files
%license Header.pm
%doc Changes README
%{perl_vendorlib}/Text/Header.pm
%{_mandir}/man3/Text::Header.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.03-1
- Package official CPAN release with its complete default test.
