# SPDX-License-Identifier: Apache-2.0
Name:           perl-Algorithm-C3
Version:        0.11
Release:        1%{?dist}
Summary:        Perl C3 method-resolution-order algorithm
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Algorithm-C3
Source0:        Algorithm-C3-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-generators

%description
Algorithm::C3 computes a consistent C3 method resolution order for
multiple-inheritance hierarchies.

%prep
%autosetup -n Algorithm-C3-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all 11 default regression files and both separately registered POD
# suites. Do not bypass the upstream SIGALRM infinite-loop regression tests.
%make_build test
%make_build test TEST_FILES="xt/*.t"

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Algorithm/C3.pm
%{_mandir}/man3/Algorithm::C3.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.11-1
- Package the official CPAN release and all default and POD test suites.
