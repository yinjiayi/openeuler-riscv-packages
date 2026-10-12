# SPDX-License-Identifier: Apache-2.0
Name:           perl-Array-Unique
Version:        0.09
Release:        1%{?dist}
Summary:        Perl tied arrays that keep unique values
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Array-Unique
Source0:        Array-Unique-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Array::Unique and its variants implement tied arrays that retain only
unique values.

%prep
%autosetup -n Array-Unique-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all four registered default t/ files and both separate POD suites.
# xt/critic.t is an optional author style check, not a functional regression;
# Test::Perl::Critic is absent from the official target repository.
./Build test
./Build test --test_files 'xt/pod.t xt/pod-coverage.t'

%files
%license README
%doc Changes README.md
%{perl_vendorlib}/Array/Unique.pm
%{perl_vendorlib}/Array/Unique/
%{_mandir}/man3/Array::Unique*.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.09-1
- Package the official CPAN release and full default and POD suites.
