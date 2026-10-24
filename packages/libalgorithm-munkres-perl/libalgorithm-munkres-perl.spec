# SPDX-License-Identifier: Apache-2.0
Name:           perl-Algorithm-Munkres
Version:        0.08
Release:        1%{?dist}
Summary:        Munkres assignment algorithm for Perl matrices
License:        GPL-2.0-or-later
URL:            https://metacpan.org/dist/Algorithm-Munkres
Source0:        Algorithm-Munkres-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Algorithm::Munkres solves minimum-cost assignment problems for square and
rectangular matrices using the Munkres algorithm.

%prep
%autosetup -n Algorithm-Munkres-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Algorithm/Munkres.pm
%{_mandir}/man3/Algorithm::Munkres.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.08-1
- Package the official CPAN release with all default upstream tests.
