# SPDX-License-Identifier: Apache-2.0
Name:           libxml-xpathengine-perl
Version:        0.14
Release:        1%{?dist}
Summary:        Evaluate XPath expressions against application node trees
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/XML-XPathEngine
Source0:        XML-XPathEngine-0.14.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(vars)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(base)
BuildRequires:  perl(overload)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
BuildRequires:  perl(Pod::Coverage)
BuildRequires:  perl(Pod::Parser)
BuildRequires:  perl(Devel::Symdump)
Requires:       perl
Requires:       perl(strict)
Requires:       perl(warnings)
Requires:       perl(vars)
Requires:       perl(Carp)
Requires:       perl(overload)
Requires:       perl(POSIX)

%description
Evaluate XPath expressions against application node trees

%prep
%autosetup -n XML-XPathEngine-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .
cat <<'DONOR_NOTICE' > XML-XPath-NOTICE
XML::XPathEngine is derived from XML::XPath by Matt Sergeant.
Copyright 2000 AxKit.com Ltd.
Redistributable under the same terms as Perl itself; see the accompanying
Artistic-1.0-Perl.txt and GPL-1.0.txt.
Reference release: https://cpan.metacpan.org/authors/id/M/MS/MSERGEANT/XML-XPath-1.13.tar.gz
DONOR_NOTICE

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/XML/XPathEngine.pm
test -f %{buildroot}%{_mandir}/man3/XML::XPathEngine.3pm

%check
make test TEST_VERBOSE=1

%files
%license README Artistic-1.0-Perl.txt GPL-1.0.txt XML-XPath-NOTICE
%doc Changes
%{perl_vendorlib}/XML/XPathEngine.pm
%{perl_vendorlib}/XML/XPathEngine/Boolean.pm
%{perl_vendorlib}/XML/XPathEngine/Expr.pm
%{perl_vendorlib}/XML/XPathEngine/Function.pm
%{perl_vendorlib}/XML/XPathEngine/Literal.pm
%{perl_vendorlib}/XML/XPathEngine/LocationPath.pm
%{perl_vendorlib}/XML/XPathEngine/NodeSet.pm
%{perl_vendorlib}/XML/XPathEngine/Number.pm
%{perl_vendorlib}/XML/XPathEngine/Root.pm
%{perl_vendorlib}/XML/XPathEngine/Step.pm
%{perl_vendorlib}/XML/XPathEngine/Variable.pm
%{_mandir}/man3/XML::XPathEngine.3pm*
%{_mandir}/man3/XML::XPathEngine::Boolean.3pm*
%{_mandir}/man3/XML::XPathEngine::Literal.3pm*
%{_mandir}/man3/XML::XPathEngine::NodeSet.3pm*
%{_mandir}/man3/XML::XPathEngine::Number.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.14-1
- Package the XPath engine, original tests, and derivative source notice.
