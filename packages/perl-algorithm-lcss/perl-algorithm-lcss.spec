# SPDX-License-Identifier: Apache-2.0
Name:           perl-Algorithm-LCSS
Version:        0.01
Release:        1%{?dist}
Summary:        Find common contiguous subsequences in strings and arrays
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Algorithm-LCSS
Source0:        Algorithm-LCSS-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Algorithm-Diff >= 1.1
BuildRequires:  perl-generators
Requires:       perl(Algorithm::Diff) >= 1.1

%description
Algorithm::LCSS uses Algorithm::Diff to find common contiguous subsequences
of strings or arrays. It provides the longest common result, all common
results, and results sorted by decreasing length.

%prep
%autosetup -n Algorithm-LCSS-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep the complete original test.pl suite: eight assertions, no exclusions.
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Algorithm/LCSS.pm
%{_mandir}/man3/Algorithm::LCSS.3*

%changelog
* Fri Nov 06 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.01-1
- Package official CPAN release with its unchanged default test suite.
