# SPDX-License-Identifier: Apache-2.0
Name:           perl-URI-Find
Version:        20160806
Release:        1%{?dist}
Summary:        Find URI references in arbitrary text
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/URI-Find
Source0:        URI-Find-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Simple
BuildRequires:  perl(URI) >= 1.60
BuildRequires:  perl-generators
Requires:       perl(URI) >= 1.60

%description
URI::Find detects URI references in arbitrary text and includes a
schemeless finder plus the urifind command-line utility.

%prep
%autosetup -n URI-Find-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all eight upstream default tests, including the nested CLI/POD tests.
./Build test

%files
%license LICENSE
%doc README Changes TODO
%{perl_vendorlib}/URI/Find.pm
%{perl_vendorlib}/URI/Find/Schemeless.pm
%{_bindir}/urifind
%{_mandir}/man1/urifind.1*
%{_mandir}/man3/URI::Find.3*
%{_mandir}/man3/URI::Find::Schemeless.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 20160806-1
- Package official CPAN URI::Find release and full recursive default test suite.
