# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-MkPasswd
Version:        0.05
Release:        1%{?dist}
Summary:        Legacy Perl password-string generator
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-MkPasswd
Source0:        String-MkPasswd-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
String::MkPasswd generates strings with configurable character classes and
includes the mkpasswd.pl command. It uses Perl's rand and must not be used
where cryptographic-strength secrets are required.

%prep
%autosetup -n String-MkPasswd-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all five upstream default t/ files, including 200 no-ambiguous
# assertions in the nested subtests of t/05ambiguous.t.
%make_build test

%files
%license LICENSE
%doc Changes README
%{_bindir}/mkpasswd.pl
%{perl_vendorlib}/String/MkPasswd.pm
%{_mandir}/man1/mkpasswd.pl.1*
%{_mandir}/man3/String::MkPasswd.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.05-1
- Package official CPAN release, command, and complete default tests.
