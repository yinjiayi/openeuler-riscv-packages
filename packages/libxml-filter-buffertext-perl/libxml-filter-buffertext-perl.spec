# SPDX-License-Identifier: Apache-2.0
Name:           libxml-filter-buffertext-perl
Version:        1.01
Release:        1%{?dist}
Summary:        Coalesce adjacent SAX character events
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/XML-Filter-BufferText
Source0:        XML-Filter-BufferText-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(XML::SAX::Base) >= 1.03
BuildRequires:  perl(XML::SAX) >= 0.04
BuildRequires:  perl(Test::More) >= 0.40
BuildRequires:  perl(base)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
Requires:       perl
Requires:       perl(XML::SAX::Base) >= 1.03
Requires:       perl(XML::SAX) >= 0.04

%description
Coalesce adjacent SAX character events

%prep
%setup -q -n XML-Filter-BufferText-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
make test

%files
%license BufferText.pm
%doc README Changes
%{perl_vendorlib}/XML/Filter/BufferText.pm
%{_mandir}/man3/XML::Filter::BufferText.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.01-1
- Package the fixed upstream release with the original test suite.
