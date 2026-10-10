# SPDX-License-Identifier: Apache-2.0
Name:           perl-Algorithm-Merge
Version:        0.08
Release:        1%{?dist}
Summary:        Three-way merge and diff routines for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Algorithm-Merge
Source0:        Algorithm-Merge-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Algorithm-Diff
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Algorithm::Diff) >= 1

%description
Algorithm::Merge provides three-way merging, three-way differences, and
sequence traversal using Algorithm::Diff.

%prep
%autosetup -n Algorithm-Merge-%{version} -p1

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
%doc CHANGES
%{perl_vendorlib}/Algorithm/Merge.pm
%{_mandir}/man3/Algorithm::Merge.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.08-1
- Package the official CPAN release with all default upstream tests.
