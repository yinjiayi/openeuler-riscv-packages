# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-WikiCreole
Version:        0.07
Release:        1%{?dist}
Summary:        Convert Wiki Creole 1.0 markup to XHTML
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-WikiCreole
Source0:        Text-WikiCreole-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Test::More)

%description
Text::WikiCreole converts Wiki Creole 1.0 markup to XHTML and supports
callbacks for custom links, images and plugin syntax.

%prep
%autosetup -n Text-WikiCreole-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all eight default upstream fixture and callback tests.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Text/WikiCreole.pm
%{_mandir}/man3/Text::WikiCreole.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.07-1
- Package official CPAN release with all eight default tests.
