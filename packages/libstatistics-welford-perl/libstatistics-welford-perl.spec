# SPDX-License-Identifier: Apache-2.0
Name:           perl-Statistics-Welford
Version:        0.02
Release:        1%{?dist}
Summary:        Online descriptive statistics using Welford's algorithm
License:        GPL-1.0-or-later
URL:            https://metacpan.org/dist/Statistics-Welford
Source0:        Statistics-Welford-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Statistics::Welford calculates count, extrema, mean, sample variance and
standard deviation incrementally without retaining the full input set.

%prep
%autosetup -n Statistics-Welford-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all three original default tests, including both POD checks.
./Build test

%files
%doc Changes
%{perl_vendorlib}/Statistics/Welford.pm
%{_mandir}/man3/Statistics::Welford.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.02-1
- Package official CPAN release with all three original default tests.
