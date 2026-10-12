# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           perl-Math-BaseCalc
Version:        1.019
Release:        1%{?dist}
Summary:        Convert numbers between arbitrary bases in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Math-BaseCalc
Source0:        Math-BaseCalc-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Carp
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Math-BigInt
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-generators

%description
Math::BaseCalc converts numbers between arbitrary positional digit sets,
including binary, octal, hexadecimal and user-defined bases.

%prep
%autosetup -n Math-BaseCalc-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all eight original t/*.t files and enable upstream's optional POD test.
# The author-only critic test retains its upstream AUTHOR_TESTING skip.
TEST_POD=1 %make_build test

%files
%license LICENSE
%doc Changes README SIGNATURE
%{perl_vendorlib}/Math/BaseCalc.pm
%{_mandir}/man3/Math::BaseCalc.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.019-1
- Package official CPAN release with complete default and POD tests.
