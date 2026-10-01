# SPDX-License-Identifier: Apache-2.0
Name:           perl-List-Pairwise
Version:        1.03
Release:        1%{?dist}
Summary:        Pairwise mapping, filtering, and search helpers for Perl lists
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/List-Pairwise
Source0:        List-Pairwise-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
List::Pairwise provides pairwise map, grep, first, last, and grouping
operations for Perl lists.

%prep
%autosetup -n List-Pairwise-%{version} -p1

%build
# The official archive bundles inc/Module/Install; Perl 5.38 does not put
# the source directory in @INC by default.
PERL5LIB=. %{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run the complete default upstream suite. warn3.t itself skips on Perl
# 5.19.006 and later because that older warnings behavior no longer applies.
%make_build test

%files
%license lib/List/Pairwise.pod
%doc Changelog
%{perl_vendorlib}/List/Pairwise.pm
%{perl_vendorlib}/List/Pairwise.pod
%{_mandir}/man3/List::Pairwise.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.03-1
- Package the official CPAN release with its full default upstream suite.
