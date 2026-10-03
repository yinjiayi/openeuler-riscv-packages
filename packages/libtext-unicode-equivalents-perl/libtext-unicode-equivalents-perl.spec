# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Unicode-Equivalents
Version:        0.05
Release:        1%{?dist}
Summary:        Generate canonically equivalent Unicode strings
License:        Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-Unicode-Equivalents
Source0:        Text-Unicode-Equivalents-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Encode
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Unicode-Normalize
BuildRequires:  perl(Unicode::UCD)
BuildRequires:  perl-generators

%description
Text::Unicode::Equivalents generates unique strings that are canonically
equivalent to an input Unicode string.

%prep
%autosetup -n Text-Unicode-Equivalents-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all 26 original Unicode-equivalence assertions.
%make_build test

%files
%doc readme.txt
%{perl_vendorlib}/Text/Unicode/Equivalents.pm
%{_mandir}/man3/Text::Unicode::Equivalents.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.05-1
- Package official CPAN release with its complete Unicode-equivalence suite.
