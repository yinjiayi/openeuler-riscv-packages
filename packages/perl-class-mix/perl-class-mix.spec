# SPDX-License-Identifier: Apache-2.0
Name:           perl-Class-Mix
Version:        0.006
Release:        1%{?dist}
Summary:        Dynamically compose Perl classes
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Mix
Source0:        Class-Mix-0.006.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl-Module-Build
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Params::Classify)
BuildRequires:  perl(parent)
BuildRequires:  perl-generators
BuildArch:      noarch
Requires:       perl

%description
Dynamically compose Perl classes

%prep
%autosetup -p1 -n Class-Mix-%{version}

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
./Build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Class/Mix.pm
%{_mandir}/man3/Class::Mix.3*

%changelog
* Fri Oct 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.006-1
- Package Class::Mix with its original tests.
