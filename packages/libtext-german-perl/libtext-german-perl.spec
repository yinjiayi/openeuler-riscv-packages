# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-German
Version:        0.06
Release:        1%{?dist}
Summary:        Approximate German word base-form reduction in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-German
Source0:        Text-German-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators

%description
Text::German approximately reduces German words to base forms and includes
an optional in-process reduction cache.

%prep
%autosetup -n Text-German-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain both upstream default suites and all 34 assertions.
%make_build test

%files
%license README
%{perl_vendorlib}/Text/German.pm
%{perl_vendorlib}/Text/German.pod
%{perl_vendorlib}/Text/German/
%{_mandir}/man3/Text::German.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.06-1
- Package official CPAN release with both full upstream tests and smoke.
