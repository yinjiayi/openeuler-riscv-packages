# SPDX-License-Identifier: Apache-2.0
Name:           perl-aliased
Version:        0.34
Release:        1%{?dist}
Summary:        Use shorter versions of Perl class names
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/aliased
Source0:        aliased-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-Module-Build-Tiny >= 0.039
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-CPAN-Meta
BuildRequires:  perl-generators

%description
The aliased pragma creates shorter aliases for long Perl class names. It
supports explicit aliases, imports and prefixes without changing the class.

%prep
%autosetup -n aliased-%{version}

%build
%{__perl} Build.PL --installdirs vendor
%{__perl} Build

%install
%{__perl} Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%{__perl} Build test

%files
%license LICENSE
%doc Changes README CONTRIBUTING
%{perl_vendorlib}/aliased.pm
%{_mandir}/man3/aliased.3*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.34-1
- Package the official CPAN release with all default tests enabled.
