# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Zglob
Version:        0.11
Release:        1%{?dist}
Summary:        Extended filesystem globbing for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Zglob
Source0:        File-Zglob-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
File::Zglob provides extended filesystem globbing, including recursive
wildcards and brace alternatives.

%prep
%autosetup -n File-Zglob-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all four default upstream t files and the declared test pattern.
%make_build test

%files
%doc README Changes
%{perl_vendorlib}/File/Zglob.pm
%{_mandir}/man3/File::Zglob.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.11-1
- Package official CPAN release and its complete default test suite.
