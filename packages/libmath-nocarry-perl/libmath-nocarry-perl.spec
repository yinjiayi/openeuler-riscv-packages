# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Math-NoCarry
Version:        1.117
Release:        1%{?dist}
Summary:        No-carry arithmetic functions for Perl
License:        Artistic-2.0
URL:            https://metacpan.org/dist/Math-NoCarry
Source0:        Math-NoCarry-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-version
BuildRequires:  perl-generators
Requires:       perl(version) >= 0.86

%description
Math::NoCarry supplies add, subtract and multiply operations that discard
digit carries.

%prep
%autosetup -n Math-NoCarry-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all six unmodified upstream default t/*.t files, including POD.
%make_build test

%files
%license LICENSE
%doc Changes README.pod SECURITY.md
%{perl_vendorlib}/Math/NoCarry.pm
%{_mandir}/man3/Math::NoCarry.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.117-1
- Package official CPAN release with complete default tests.
