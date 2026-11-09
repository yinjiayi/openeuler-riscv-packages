# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-useallmodules
Version:        0.17
Release:        1%{?dist}
Summary:        Check that all Perl modules listed in a distribution can load
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Test-UseAllModules
Source0:        https://cpan.metacpan.org/authors/id/I/IS/ISHIGAKI/Test-UseAllModules-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More) >= 0.60
BuildRequires:  perl(Test::Builder) >= 0.30
BuildRequires:  perl(ExtUtils::Manifest)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Test::Pod) >= 1.18
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
Requires:       perl
Requires:       perl(ExtUtils::Manifest)
Requires:       perl(Exporter)
Requires:       perl(Test::More) >= 0.60
Requires:       perl(Test::Builder) >= 0.30

%description
Use a distribution's MANIFEST to discover Perl modules and check that
each selected module can load.

%prep
%setup -q -n Test-UseAllModules-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR="%{buildroot}"

%check
make test

%files
%license README
%doc Changes
%{perl_vendorlib}/Test/UseAllModules.pm
%{_mandir}/man3/Test::UseAllModules.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.17-1
- Package the fixed release and retain the unchanged upstream default tests.
