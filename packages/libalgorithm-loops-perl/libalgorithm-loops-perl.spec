# SPDX-License-Identifier: Apache-2.0
Name:           perl-Algorithm-Loops
Version:        1.032
Release:        1%{?dist}
Summary:        Looping and permutation constructs for Perl
License:        Unlicense
URL:            https://metacpan.org/dist/Algorithm-Loops
Source0:        Algorithm-Loops-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators

%description
Algorithm::Loops offers filtering, mapping, nested looping, and
permutation helpers for Perl programs.

%prep
%autosetup -n Algorithm-Loops-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run both upstream t/ files, including all 111 assertions.
%make_build test

%files
%license LICENSE
%doc Changes README.txt
%{perl_vendorlib}/Algorithm/Loops.pm
%{_mandir}/man3/Algorithm::Loops.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.032-1
- Package the official CPAN release and complete default test suite.
