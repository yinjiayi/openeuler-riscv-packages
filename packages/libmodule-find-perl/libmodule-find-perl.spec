# SPDX-License-Identifier: Apache-2.0
Name:           perl-module-find
Version:        0.17
Release:        1%{?dist}
Summary:        Find and load installed Perl modules by namespace
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND GPL-3.0-only
URL:            https://metacpan.org/dist/Module-Find
Source0:        Module-Find-0.17.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
Source3:        GPL-3.0.txt
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::CPAN::Meta)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl(Test::Pod::Coverage) >= 1.04
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl
Requires:       perl(Exporter)
Requires:       perl(File::Find)
Requires:       perl(File::Spec)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Module::Find locates installed Perl modules below a namespace and can
optionally load them. It supports direct children and recursive searches.

%prep
%autosetup -n Module-Find-%{version} -p1
install -pm0644 %{SOURCE1} Artistic-1.0-Perl.txt
install -pm0644 %{SOURCE2} GPL-1.0.txt
install -pm0644 %{SOURCE3} GPL-3.0.txt
cat <<'DONOR_NOTICE' > EUMM-Upgrade-NOTICE
Makefile.PL includes the build-only WriteMakefile1 helper, version 0.21.
Copyright 2009 Alexandr Ciornii.
License: GPL-3.0-only (see GPL-3.0.txt).
Donor: https://cpan.metacpan.org/authors/id/C/CH/CHORNY/App-EUMM-Upgrade-0.21.tar.gz
The helper is not installed as part of the Perl module.
DONOR_NOTICE

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/Module/Find.pm
test -f %{buildroot}%{_mandir}/man3/Module::Find.3pm

%check
make test TEST_VERBOSE=1

%files
%license README Artistic-1.0-Perl.txt GPL-1.0.txt GPL-3.0.txt EUMM-Upgrade-NOTICE
%doc Changes examples/example.pl
%{perl_vendorlib}/Module/Find.pm
%{_mandir}/man3/Module::Find.3pm*

%changelog
* Wed Nov 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.17-1
- Package the fixed CPAN release and retain all original default tests.
