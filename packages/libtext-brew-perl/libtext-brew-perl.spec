# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Brew
Version:        0.02
Release:        1%{?dist}
Summary:        Calculate Brew edit distance and edit operations
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-Brew
Source0:        Text-Brew-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-generators
Requires:       perl(Test::More)

%description
Text::Brew calculates the edit distance between strings and can return
the sequence of insertion, deletion, match and substitution operations.

%prep
%autosetup -n Text-Brew-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all three default upstream suites; Test::Pod is required so pod.t
# runs rather than reporting an optional dependency SKIP.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Text/Brew.pm
%{_mandir}/man3/Text::Brew.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.02-1
- Package official CPAN release with all three default suites, including POD.
