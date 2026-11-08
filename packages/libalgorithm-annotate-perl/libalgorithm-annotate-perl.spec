# SPDX-License-Identifier: Apache-2.0
Name:           perl-Algorithm-Annotate
Version:        0.10
Release:        1%{?dist}
Summary:        Represent changes in an annotated sequence with Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Algorithm-Annotate
Source0:        Algorithm-Annotate-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Algorithm-Diff
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl(Algorithm::Diff) >= 1.15

%description
Algorithm::Annotate tracks successive sequence revisions and attributes each
item to the revision that introduced or changed it.

%prep
%autosetup -n Algorithm-Annotate-%{version} -p1

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
%license Annotate.pm
%{perl_vendorlib}/Algorithm/Annotate.pm
%{_mandir}/man3/Algorithm::Annotate.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.10-1
- Package the official CPAN release with the complete default upstream test.
