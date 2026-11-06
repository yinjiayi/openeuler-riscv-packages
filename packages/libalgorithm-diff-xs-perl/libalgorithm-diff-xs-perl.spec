# SPDX-License-Identifier: Apache-2.0
Name:           perl-Algorithm-Diff-XS
Version:        0.04
Release:        1%{?dist}
Summary:        XS implementation of Algorithm::Diff core loops
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Algorithm-Diff-XS
Source0:        Algorithm-Diff-XS-%{version}.tar.gz

BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Algorithm-Diff
BuildRequires:  perl-Data-Dumper
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-ExtUtils-ParseXS
BuildRequires:  perl-devel
BuildRequires:  perl-generators
Requires:       perl(Algorithm::Diff) >= 1.19

%description
Algorithm::Diff::XS provides an XS core loop for Algorithm::Diff and exposes
its diff, longest-common-subsequence, and traversal interfaces.

%prep
%autosetup -n Algorithm-Diff-XS-%{version} -p1

%build
# The verified source archive includes its bundled inc/Module/Install code.
%{__perl} -I. Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
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
%{perl_vendorarch}/Algorithm/Diff/XS.pm
%{perl_vendorarch}/auto/Algorithm/Diff/XS/
%{_mandir}/man3/Algorithm::Diff::XS.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.04-1
- Package the official CPAN XS release with all default upstream tests.
