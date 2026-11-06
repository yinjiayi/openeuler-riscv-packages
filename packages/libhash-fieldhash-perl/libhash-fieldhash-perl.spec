# SPDX-License-Identifier: Apache-2.0
Name:           perl-Hash-FieldHash
Version:        0.15
Release:        1%{?dist}
Summary:        Lightweight field hashes for Perl objects
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Hash-FieldHash
Source0:        Hash-FieldHash-%{version}.tar.gz

BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-Devel-PPPort
BuildRequires:  perl-ExtUtils-CBuilder
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-ExtUtils-ParseXS
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Scalar-List-Utils
BuildRequires:  perl-Test-LeakTrace
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-parent
BuildRequires:  perl-threads
BuildRequires:  perl-generators

%description
Hash::FieldHash provides field hashes whose object-keyed entries are
automatically released when the corresponding objects are destroyed.

%prep
%autosetup -n Hash-FieldHash-%{version} -p1

%build
# The verified archive's Build.PL imports its bundled builder/MyBuilder.pm.
%{__perl} -I. Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
./Build test

%files
%license LICENSE
%doc Changes README.md
%{perl_vendorarch}/Hash/FieldHash.pm
%{perl_vendorarch}/auto/Hash/FieldHash/
%{_mandir}/man3/Hash::FieldHash.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.15-1
- Package the official CPAN XS release with all default upstream tests.
