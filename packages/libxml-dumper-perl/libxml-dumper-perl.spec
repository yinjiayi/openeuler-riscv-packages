# SPDX-License-Identifier: Apache-2.0
Name:           libxml-dumper-perl
Version:        0.81
Release:        1%{?dist}
Summary:        Serialize Perl data structures as XML and read them back
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/XML-Dumper
Source0:        XML-Dumper-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(XML::Parser) >= 2.16
BuildRequires:  perl(Compress::Zlib)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(lib)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
Requires:       perl
Requires:       perl(XML::Parser) >= 2.16
Requires:       perl(Compress::Zlib)

%description
Serialize Perl data structures as XML and read them back, including
plain XML and gzip-compressed files.

%prep
%setup -q -n XML-Dumper-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
make test

%files
%license README
%doc Changes
%{perl_vendorlib}/XML/Dumper.pm
%{_mandir}/man3/XML::Dumper.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.81-1
- Package the pinned release and retain all original tests, including compression and UTF-8.
