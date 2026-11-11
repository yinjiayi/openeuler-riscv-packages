# SPDX-License-Identifier: Apache-2.0
Name:           perl-Array-Shuffle
Version:        0.04
Release:        1%{?dist}
Summary:        Shuffle Perl arrays in place
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Array-Shuffle
Source0:        Array-Shuffle-0.04.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test::More)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl-generators
Requires:       perl

%description
Shuffle Perl arrays in place

%prep
%autosetup -p1 -n Array-Shuffle-%{version}

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
%license README ppport.h
%doc Changes
%{perl_vendorarch}/Array/Shuffle.pm
%{perl_vendorarch}/auto/Array/Shuffle/
%{_mandir}/man3/Array::Shuffle.3*

%changelog
* Fri Oct 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.04-1
- Package Array::Shuffle with its original tests.
