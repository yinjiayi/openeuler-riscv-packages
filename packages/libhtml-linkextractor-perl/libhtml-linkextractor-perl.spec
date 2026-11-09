# SPDX-License-Identifier: Apache-2.0
Name:           libhtml-linkextractor-perl
Version:        0.13
Release:        1%{?dist}
Summary:        Extract links and attributes from HTML in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/HTML-LinkExtractor
Source0:        HTML-LinkExtractor-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl-Test-Harness
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(HTML::TokeParser) >= 2
BuildRequires:  perl(Test)
BuildRequires:  perl(URI) >= 1
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(HTML::TokeParser) >= 2
Requires:       perl(URI) >= 1

%description
Extract links and related attributes from HTML in Perl, with optional
visible-text extraction and callback-based processing.

%prep
%setup -q -n HTML-LinkExtractor-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
make test
prove -Iblib/lib -Iblib/arch ./test.pl

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/HTML/LinkExtractor.pm
%{_mandir}/man3/HTML::LinkExtractor.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.13-1
- Package the pinned release and run all original assertions.
