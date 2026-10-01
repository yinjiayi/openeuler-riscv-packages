# SPDX-License-Identifier: Apache-2.0
Name:           perl-List-Compare
Version:        0.55
Release:        1%{?dist}
Summary:        Compare elements of two or more Perl lists
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/List-Compare
Source0:        List-Compare-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Capture-Tiny
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
List::Compare compares the contents of two or more Perl lists and reports
intersections, unions, unique elements, complements and subset relations.
It offers object-oriented and functional interfaces.

%prep
%autosetup -n List-Compare-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all 52 default upstream test files, including error paths.
%make_build test

%files
%license README
%doc Changes FAQ
%{perl_vendorlib}/List/Compare.pm
%{perl_vendorlib}/List/Compare/
%{_mandir}/man3/List::Compare*.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.55-1
- Package official CPAN release and retain the complete upstream suite.
