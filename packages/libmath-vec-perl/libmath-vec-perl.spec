# SPDX-License-Identifier: Apache-2.0
Name:           perl-Math-Vec
Version:        1.01
Release:        1%{?dist}
Summary:        Three-dimensional vector arithmetic for Perl
License:        Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Math-Vec
Source0:        Math-Vec-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
Requires:       perl

%description
Math::Vec provides object-oriented three-dimensional vector arithmetic,
including length, dot and cross products, angles, and projections.

%prep
%autosetup -n Math-Vec-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run every unchanged upstream default t/ file.
./Build test

%files
%license lib/Math/Vec.pm
%doc README Changes
%{perl_vendorlib}/Math/Vec.pm
%{_mandir}/man3/Math::Vec.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.01-1
- Package official CPAN release and all default tests.
