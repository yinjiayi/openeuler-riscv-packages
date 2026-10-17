# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-TreeCreate
Version:        0.0.1
Release:        1%{?dist}
Summary:        Recursively create and populate directory trees in Perl
License:        MIT
URL:            https://metacpan.org/dist/File-TreeCreate
Source0:        File-TreeCreate-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
File::TreeCreate creates nested directories and files from a tree description
and provides helpers to inspect and read the resulting tree.

%prep
%autosetup -n File-TreeCreate-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain both default upstream tests: one compile plus 22 tree assertions.
./Build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/File/TreeCreate.pm
%{_mandir}/man3/File::TreeCreate.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.1-1
- Package official CPAN release with its complete upstream test suite.
