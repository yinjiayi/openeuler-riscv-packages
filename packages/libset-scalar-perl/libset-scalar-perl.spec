# SPDX-License-Identifier: Apache-2.0
Name:           perl-Set-Scalar
Version:        1.29
Release:        1%{?dist}
Summary:        Set operations on Perl scalars
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Set-Scalar
Source0:        Set-Scalar-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl-generators
Requires:       perl(Scalar::Util)

%description
Set::Scalar supplies scalar-set membership, union, intersection, difference,
and related algebraic operations through a pure-Perl implementation.

%prep
%autosetup -n Set-Scalar-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep and execute all 22 original default t/ files without alteration.
%make_build test

%files
%license lib/Set/Scalar.pm
%doc README ChangeLog
%{perl_vendorlib}/Set/Scalar.pm
%{perl_vendorlib}/Set/Scalar/
%{_mandir}/man3/Set::Scalar*.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.29-1
- Package the official CPAN release and all original tests.
