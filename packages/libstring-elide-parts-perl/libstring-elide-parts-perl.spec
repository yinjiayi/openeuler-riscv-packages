# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-Elide-Parts
Version:        0.07
Release:        1%{?dist}
Summary:        Elide parts of Perl strings to a desired display length
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-Elide-Parts
Source0:        String-Elide-Parts-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
String::Elide::Parts shortens text to a desired display length by removing
characters from the left, right, middle, or ends. It also supports markup
that prioritizes which spans to shorten first.

%prep
%autosetup -n String-Elide-Parts-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve unmodified defaults: two operational files run; the two
# author-only files explicitly skip unless AUTHOR_TESTING is set upstream.
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/String/Elide/Parts.pm
%{_mandir}/man3/String::Elide::Parts.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.07-1
- Package official CPAN release with unmodified upstream default suites.
