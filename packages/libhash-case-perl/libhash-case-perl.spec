# SPDX-License-Identifier: Apache-2.0
Name:           perl-Hash-Case
Version:        1.07
Release:        1%{?dist}
Summary:        Tied hashes with configurable key casing
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Hash-Case
Source0:        Hash-Case-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Hash::Case provides tied hashes that normalize keys to lower or upper case,
or retain the original key while permitting case-insensitive lookup.

%prep
%autosetup -n Hash-Case-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all four default upstream test files and 140 assertions.
%make_build test

%files
%license README.md
%doc README ChangeLog
%{perl_vendorlib}/Hash/Case.pm
%{perl_vendorlib}/Hash/Case.pod
%{perl_vendorlib}/Hash/Case/
%{_mandir}/man3/Hash::Case*.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.07-1
- Package official CPAN release and retain the complete default upstream suite.
