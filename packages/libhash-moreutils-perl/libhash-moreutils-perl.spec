# SPDX-License-Identifier: Apache-2.0
Name:           perl-Hash-MoreUtils
Version:        0.06
Release:        1%{?dist}
Summary:        Additional utility functions for Perl hashes
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Hash-MoreUtils
Source0:        Hash-MoreUtils-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Hash::MoreUtils supplies commonly used operations for Perl hashes, including
key slicing, filtering, sorting and safe reversal.

%prep
%autosetup -n Hash-MoreUtils-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain both default upstream test files and 66 assertions.
%make_build test

%files
%license README.md
%doc Changes
%{perl_vendorlib}/Hash/MoreUtils.pm
%{_mandir}/man3/Hash::MoreUtils*.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.06-1
- Package official CPAN release and retain the complete default upstream suite.
