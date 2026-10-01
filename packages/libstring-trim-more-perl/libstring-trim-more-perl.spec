# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-Trim-More
Version:        0.03
Release:        1%{?dist}
Summary:        Additional trimming and ellipsis helpers for Perl strings
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-Trim-More
Source0:        String-Trim-More-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
String::Trim::More provides whole-string and per-line whitespace trimming,
blank-line trimming and ellipsis shortening. It is distinct from
String::Trim.

%prep
%autosetup -n String-Trim-More-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve unmodified defaults: two operational files run; two author-only
# files explicitly skip unless AUTHOR_TESTING is set upstream.
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/String/Trim/More.pm
%{_mandir}/man3/String::Trim::More.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.03-1
- Package official CPAN release with unmodified default operational tests.
