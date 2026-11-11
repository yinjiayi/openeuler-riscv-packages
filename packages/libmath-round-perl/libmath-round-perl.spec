# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Math-Round
Version:        0.08
Release:        1%{?dist}
Summary:        Rounding functions for Perl numbers
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Math-Round
Source0:        Math-Round-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Math::Round provides several number-rounding functions, including nearest
multiple, even/odd tie handling, ceiling and floor variants.

%prep
%autosetup -n Math-Round-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve the unmodified upstream default test file and all ten assertions.
%make_build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Math/Round.pm
%{_mandir}/man3/Math::Round.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.08-1
- Package official CPAN release with its complete default test suite.
