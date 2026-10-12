# SPDX-License-Identifier: Apache-2.0
Name:           perl-Hash-Ordered
Version:        0.014
Release:        1%{?dist}
Summary:        Fast pure-Perl ordered hash class
License:        Apache-2.0
URL:            https://metacpan.org/dist/Hash-Ordered
Source0:        Hash-Ordered-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Carp
BuildRequires:  perl-constant
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Scalar-List-Utils
BuildRequires:  perl-Test-Deep
BuildRequires:  perl-Test-FailWarnings
BuildRequires:  perl-Test-Fatal
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Hash::Ordered stores key/value pairs while preserving insertion order. It
offers direct and tied-hash interfaces, ordered iteration and cloning.

%prep
%autosetup -n Hash-Ordered-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all four default upstream test files and 112 assertions.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Hash/Ordered.pm
%{perl_vendorlib}/Hash/Ordered/
%{_mandir}/man3/Hash::Ordered*.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.014-1
- Package official CPAN release and retain the complete default upstream suite.
