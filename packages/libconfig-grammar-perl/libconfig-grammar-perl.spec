# SPDX-License-Identifier: Apache-2.0
Name:           libconfig-grammar-perl
Version:        1.13
Release:        1%{?dist}
Summary:        Parse configuration files using a user-friendly Perl grammar
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Config-Grammar
Source0:        Config-Grammar-%{version}.tar.gz
Patch0:         0001-retain-makemaker-template-license.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::Simple)
BuildRequires:  perl(base)
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
Requires:       perl

%description
Parse and validate configuration files against a Perl grammar. Generate
configuration documentation and templates from the same grammar.

%prep
%autosetup -p1 -n Config-Grammar-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
make test

%files
%license LICENSE LICENSE.MakeMaker-template
%doc README Changes
%{perl_vendorlib}/Config/Grammar.pm
%{perl_vendorlib}/Config/Grammar/
%{_mandir}/man3/Config::Grammar.3pm*
%{_mandir}/man3/Config::Grammar::Dynamic.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.13-1
- Package the pinned release with all original tests and template notice.
