# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-FindIndent
Version:        0.12
Release:        1%{?dist}
Summary:        Detect the indentation style used in text
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-FindIndent
Source0:        Text-FindIndent-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Text::FindIndent detects whether a text document uses spaces, tabs or mixed
indentation and estimates the indentation width.

%prep
%autosetup -n Text-FindIndent-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep both upstream default test files, including all 20 fixture cases.
%make_build test

%files
%license LICENSE
%doc Changes
%{perl_vendorlib}/Text/FindIndent.pm
%{_mandir}/man3/Text::FindIndent.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.12-1
- Package official CPAN release with the complete upstream default test suite.
