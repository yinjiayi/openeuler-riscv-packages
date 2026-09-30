# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-TabularDisplay
Version:        1.38
Release:        1%{?dist}
Summary:        Display text as a formatted table in Perl
License:        GPL-2.0-only
URL:            https://metacpan.org/dist/Text-TabularDisplay
Source0:        Text-TabularDisplay-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test)
BuildRequires:  perl-generators

%description
Text::TabularDisplay arranges columns and rows into a bordered text table.

%prep
%autosetup -n Text-TabularDisplay-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all 17 default upstream t/ tests.
%make_build test

%files
%license COPYING
%doc README
%{perl_vendorlib}/Text/TabularDisplay.pm
%{_mandir}/man3/Text::TabularDisplay.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.38-1
- Package the official CPAN release with all default upstream tests.
