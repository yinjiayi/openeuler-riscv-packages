# SPDX-License-Identifier: Apache-2.0
Name:           perl-List-Gen
Version:        0.979
Release:        1%{?dist}
Summary:        Lazy list generators and operations for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/List-Gen
Source0:        List-Gen-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Filter-Simple
BuildRequires:  perl-Scalar-List-Utils
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Pod-Coverage
BuildRequires:  perl-generators

%description
List::Gen supplies lazy list generators, composable list operations, and
related utility modules for Perl.

%prep
%autosetup -n List-Gen-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run every default upstream test, including POD and POD coverage. The
# upstream manifest author checks remain conditional on RELEASE_TESTING.
%make_build test

%files
%license lib/List/Gen.pm
%doc README Changes
%{perl_vendorlib}/List/Gen.pm
%{perl_vendorlib}/List/Generator.pm
%{perl_vendorlib}/List/Gen/
%{_mandir}/man3/List::Gen*.3*
%{_mandir}/man3/List::Generator.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.979-1
- Package official CPAN stable release with the complete default test suite.
