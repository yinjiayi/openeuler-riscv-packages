# SPDX-License-Identifier: Apache-2.0
Name:           perl-Statistics-Contingency
Version:        0.09
Release:        1%{?dist}
Summary:        Precision and recall metrics from contingency tables
License:        GPL-1.0-or-later
URL:            https://metacpan.org/dist/Statistics-Contingency
Source0:        Statistics-Contingency-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Params-Validate
BuildRequires:  perl-generators
Requires:       perl(Params::Validate)

%description
Statistics::Contingency calculates precision, recall, F1, accuracy and
error metrics from category-assignment contingency tables.

%prep
%autosetup -n Statistics-Contingency-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain both original default test files; the author-only test self-skips.
./Build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Statistics/Contingency.pm
%{_mandir}/man3/Statistics::Contingency.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.09-1
- Package official CPAN release with unchanged default tests.
