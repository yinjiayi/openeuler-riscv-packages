# SPDX-License-Identifier: Apache-2.0
Name:           perl-Hash-MultiValue
Version:        0.16
Release:        1%{?dist}
Summary:        Store multiple values for each Perl hash key
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Hash-MultiValue
Source0:        Hash-MultiValue-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Carp
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Scalar-List-Utils
BuildRequires:  perl-Storable
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
BuildRequires:  perl-threads

%description
Hash::MultiValue stores multiple values under a single key while supporting
ordinary hash-style access to the latest value.

%prep
%autosetup -n Hash-MultiValue-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all ten default upstream files and their original skip conditions.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Hash/MultiValue.pm
%{_mandir}/man3/Hash::MultiValue*.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.16-1
- Package official CPAN release and retain the complete default upstream suite.
