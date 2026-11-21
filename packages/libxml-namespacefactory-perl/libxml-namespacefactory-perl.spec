# SPDX-License-Identifier: Apache-2.0
Name:           libxml-namespacefactory-perl
Version:        1.02
Release:        1%{?dist}
Summary:        Construct Clark names from XML namespaces
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/XML-NamespaceFactory
Source0:        XML-NamespaceFactory-1.02.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.17
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(Carp)
BuildRequires:  perl(overload)
BuildRequires:  perl(vars)
BuildRequires:  perl(Test)
Requires:       perl
Requires:       perl(strict)
Requires:       perl(Carp)
Requires:       perl(overload)
Requires:       perl(vars)

%description
Construct Clark names from XML namespaces

%prep
%autosetup -n XML-NamespaceFactory-%{version} -p1
cat <<'DONOR_NOTICE' > Dist-Zilla-NOTICE
The Makefile.PL template is from the MakeMaker plugin in Dist-Zilla 5.019.
Copyright (c) 2014 by Ricardo SIGNES.
Redistributable under the same terms as Perl 5; see the accompanying LICENSE.
Source: https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Dist-Zilla-5.019.tar.gz
DONOR_NOTICE

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/XML/NamespaceFactory.pm
test -f %{buildroot}%{_mandir}/man3/XML::NamespaceFactory.3pm

%check
make test TEST_VERBOSE=1

%files
%license LICENSE Dist-Zilla-NOTICE
%doc README Changes
%{perl_vendorlib}/XML/NamespaceFactory.pm
%{_mandir}/man3/XML::NamespaceFactory.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.02-1
- Package the original module, tests, and MakeMaker template notice.
