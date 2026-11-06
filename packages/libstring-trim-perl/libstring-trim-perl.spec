# SPDX-License-Identifier: Apache-2.0
Name:           perl-String-Trim
Version:        0.005
Release:        1%{?dist}
Summary:        Trim whitespace from Perl strings and containers
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/String-Trim
Source0:        String-Trim-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
String::Trim trims surrounding whitespace from strings and supports array
and hash values. It is a distinct Perl module from Text::Trim.

%prep
%autosetup -n String-Trim-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all nine upstream default t/*.t files; xt author/release suites are
# nondefault and are not presented as functional passes.
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/String/Trim.pm
%{_mandir}/man3/String::Trim.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.005-1
- Package official CPAN release with all nine default upstream test files.
