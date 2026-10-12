# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-sprintfn
Version:        0.090
Release:        1%{?dist}
Summary:        Perl sprintf with named parameter support
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-sprintfn
Source0:        Text-sprintfn-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Text::sprintfn provides sprintfn and printfn, adding named parameters to
Perl string formatting.

%prep
%autosetup -n Text-sprintfn-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain upstream's default test contract unchanged: 00-compile and 01-basics
# run 30 assertions. Three author-only files skip without AUTHOR_TESTING.
# Two historical cases in 01-basics are commented upstream, not tested here.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Text/sprintfn.pm
%{_mandir}/man3/Text::sprintfn.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.090-1
- Package official CPAN release retaining its default upstream tests.
