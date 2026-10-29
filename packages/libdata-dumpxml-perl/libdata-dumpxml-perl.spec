# SPDX-License-Identifier: Apache-2.0
Name:           perl-Data-DumpXML
Version:        1.06
Release:        1%{?dist}
Summary:        Serialize Perl data structures as XML and restore them
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-DumpXML
Source0:        Data-DumpXML-1.06.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(XML::Parser)
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(Array::RefElem)
BuildRequires:  perl-generators
BuildArch:      noarch
Requires:       perl
Requires:       perl(XML::Parser)
Requires:       perl(MIME::Base64)
Requires:       perl(Array::RefElem)

%description
Serialize Perl data structures as XML and restore them

%prep
%autosetup -p1 -n Data-DumpXML-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license README
%doc Changes Data-DumpXML.dtd Data-DumpXML.xsd
%{perl_vendorlib}/Data/DumpXML.pm
%{perl_vendorlib}/Data/DumpXML/
%{_mandir}/man3/Data::DumpXML.3*
%{_mandir}/man3/Data::DumpXML::Parser.3*

%changelog
* Fri Oct 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.06-1
- Package Data::DumpXML with its original tests.
