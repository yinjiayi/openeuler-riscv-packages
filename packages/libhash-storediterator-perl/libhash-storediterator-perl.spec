# SPDX-License-Identifier: Apache-2.0
Name:           perl-Hash-StoredIterator
Version:        0.008
Release:        1%{?dist}
Summary:        Independent iterators over Perl hash entries
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Hash-StoredIterator
Source0:        Hash-StoredIterator-%{version}.tar.gz

BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-CBuilder
BuildRequires:  perl-ExtUtils-ParseXS
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test2-Suite
BuildRequires:  perl-generators

%description
Hash::StoredIterator saves and restores a hash's iterator state so that
independent and nested iterations do not interfere with one another.

%prep
%autosetup -n Hash-StoredIterator-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
./Build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorarch}/Hash/StoredIterator.pm
%{perl_vendorarch}/auto/Hash/StoredIterator/
%{_mandir}/man3/Hash::StoredIterator.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.008-1
- Package the official CPAN XS release with all default upstream tests.
