# SPDX-License-Identifier: Apache-2.0
Name:           perl-Algorithm-NaiveBayes
Version:        0.04
Release:        1%{?dist}
Summary:        Bayesian category prediction in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Algorithm-NaiveBayes
Source0:        Algorithm-NaiveBayes-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-PathTools
BuildRequires:  perl-Scalar-List-Utils
BuildRequires:  perl-Storable
BuildRequires:  perl-generators

%description
Algorithm::NaiveBayes trains Bayesian category models and predicts labels
from observed attributes.

%prep
%autosetup -n Algorithm-NaiveBayes-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all three upstream t/ files, including the state roundtrip test.
%make_build test

%files
%doc Changes INSTALL
%{perl_vendorlib}/Algorithm/NaiveBayes.pm
%{perl_vendorlib}/Algorithm/NaiveBayes/
%{_mandir}/man3/Algorithm::NaiveBayes.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.04-1
- Package the official CPAN release and complete default test suite.
