# SPDX-License-Identifier: Apache-2.0
Name:           perl-string-approx
Version:        3.28
Release:        1%{?dist}
Summary:        Approximate string matching for Perl
License:        LGPL-2.0-only
URL:            https://metacpan.org/dist/String-Approx
Source0:        String-Approx-3.28.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
BuildRequires:  findutils


%description
String::Approx implements approximate string matching, indexing, substitution
and edit-distance operations with a C engine exposed through Perl XS.

%prep
%autosetup -n String-Approx-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="%{optflags}"
%make_build

%install
%make_install
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete
find %{buildroot} -type f -name '*.bs' -size 0 -delete

%check
%make_build test

%files
%license COPYRIGHT COPYRIGHT.agrep LGPL Artistic README.apse
%doc README ChangeLog PROBLEMS
%{perl_vendorarch}/String/Approx.pm
%{perl_vendorarch}/auto/String/Approx/
%{_mandir}/man3/String::Approx.3*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.28-1
- Package the fixed official source with all original default tests and notices.
