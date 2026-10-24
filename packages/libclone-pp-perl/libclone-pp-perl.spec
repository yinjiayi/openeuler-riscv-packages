# SPDX-License-Identifier: Apache-2.0
Name:           perl-Clone-PP
Version:        1.09
Release:        1%{?dist}
Summary:        Pure-Perl cloning of nested data structures
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Clone-PP
Source0:        Clone-PP-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Data-Dumper
BuildRequires:  perl-Test-Simple
BuildRequires:  perl(Benchmark)
BuildRequires:  perl-generators

%description
Clone::PP supplies a pure-Perl clone function for nested arrays, hashes,
objects, and scalar references. It can provide a cloning backend without
an XS implementation.

%prep
%autosetup -n Clone-PP-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all seven original default upstream files, including its two known
# TODO diagnostics for references to hash elements.
%make_build test

%files
%doc README Changes
%{perl_vendorlib}/Clone/PP.pm
%{_mandir}/man3/Clone::PP.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.09-1
- Package official CPAN release with all original default upstream tests.
