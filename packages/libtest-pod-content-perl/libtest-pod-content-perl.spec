# SPDX-License-Identifier: Apache-2.0
Name:           perl-Test-Pod-Content
Version:        0.0.6
Release:        1%{?dist}
Summary:        Test the contents of Perl POD documentation
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Test-Pod-Content
Source0:        Test-Pod-Content-v%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Pod-Simple
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-version
BuildRequires:  perl-generators

%description
Test::Pod::Content checks the text in named sections of Perl POD
documentation from a Perl test suite.

%prep
%autosetup -n Test-Pod-Content-v%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all seven upstream default tests and their original author-test gates.
./Build test

%files
%doc README Changes HACKING
%{perl_vendorlib}/Test/Pod/Content.pm
%{_mandir}/man3/Test::Pod::Content.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.6-1
- Package official CPAN v0.0.6 source with all default upstream tests.
