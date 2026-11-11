# SPDX-License-Identifier: Apache-2.0
Name:           perl-Array-RefElem
Version:        1.00
Release:        1%{?dist}
Summary:        Store references to values in Perl arrays and hashes
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Array-RefElem
Source0:        Array-RefElem-1.00.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
Requires:       perl

%description
Store references to values in Perl arrays and hashes

%prep
%autosetup -p1 -n Array-RefElem-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 OPTIMIZE="%{optflags}"
%make_build

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name '*.bs' -size 0 -delete
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%make_build test

%files
%license README
%doc Changes
%{perl_vendorarch}/Array/RefElem.pm
%{perl_vendorarch}/auto/Array/RefElem/
%{_mandir}/man3/Array::RefElem.3*

%changelog
* Thu Oct 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.00-1
- Package Array::RefElem with its upstream test suite.
