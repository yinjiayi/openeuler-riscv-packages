# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-Tokenizer
Version:        0.06
Release:        1%{?dist}
Summary:        Tokenize Perl strings with configurable delimiters
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-Tokenizer
Source0:        String-Tokenizer-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
String::Tokenizer splits text into tokens using configurable delimiters and
provides a token iterator with navigation and collection operations.

%prep
%autosetup -n String-Tokenizer-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve the unmodified defaults: two operational suites run; two
# release-candidate-only POD suites explicitly skip under upstream rules.
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/String/Tokenizer.pm
%{_mandir}/man3/String::Tokenizer.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.06-1
- Package official CPAN release with unmodified upstream default suites.
