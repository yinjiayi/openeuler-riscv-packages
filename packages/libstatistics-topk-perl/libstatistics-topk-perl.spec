# SPDX-License-Identifier: Apache-2.0
Name:           perl-Statistics-TopK
Version:        0.02
Release:        1%{?dist}
Summary:        Bounded-memory top-k stream counters
License:        GPL-1.0-or-later
URL:            https://metacpan.org/dist/Statistics-TopK
Source0:        Statistics-TopK-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
Statistics::TopK implements a bounded-memory stream counter that tracks
candidate frequent elements without retaining every input item.

%prep
%autosetup -n Statistics-TopK-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run the unchanged upstream default t/*.t suite.
%make_build test

%files
%doc Changes README
%{perl_vendorlib}/Statistics/TopK.pm
%{_mandir}/man3/Statistics::TopK.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.02-1
- Package official CPAN release with all three original default tests.
