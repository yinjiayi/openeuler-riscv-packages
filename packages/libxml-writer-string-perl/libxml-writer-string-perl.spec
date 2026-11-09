# SPDX-License-Identifier: Apache-2.0
Name:           libxml-writer-string-perl
Version:        0.1
Release:        1%{?dist}
Summary:        Capture XML::Writer output in a Perl scalar
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/XML-Writer-String
Source0:        XML-Writer-String-0.1.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(XML::Writer)
BuildRequires:  perl(Test)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl
Requires:       perl(XML::Writer)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Capture XML::Writer output in a Perl scalar

%prep
%autosetup -n XML-Writer-String-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/XML/Writer/String.pm
test -f %{buildroot}%{_mandir}/man3/XML::Writer::String.3pm

%check
make test TEST_VERBOSE=1

%files
%license README Artistic-1.0-Perl.txt GPL-1.0.txt
%doc Changes
%{perl_vendorlib}/XML/Writer/String.pm
%{_mandir}/man3/XML::Writer::String.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1-1
- Package the original Perl source and test, not the historical PPM bundle.
