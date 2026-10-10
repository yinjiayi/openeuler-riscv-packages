# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-SearchPath
Version:        0.07
Release:        1%{?dist}
Summary:        Search for files in a PATH-like environment variable
License:        GPL-2.0-or-later
URL:            https://metacpan.org/dist/File-SearchPath
Source0:        File-SearchPath-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
File::SearchPath locates files or directories through a PATH-like
environment variable, returning the first match or all matches.

%prep
%autosetup -n File-SearchPath-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run the complete single-file default upstream suite of 16 tests.
./Build test

%files
%license README
%doc ChangeLog
%{perl_vendorlib}/File/SearchPath.pm
%{_mandir}/man3/File::SearchPath.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.07-1
- Package official CPAN release with its complete default upstream suite.
