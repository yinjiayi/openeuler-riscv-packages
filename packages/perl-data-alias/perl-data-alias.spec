# SPDX-License-Identifier: Apache-2.0
Name:           perl-Data-Alias
Version:        1.30
Release:        1%{?dist}
Summary:        Perl aliasing operations for scalars and data structures
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Alias
Source0:        Data-Alias-1.30.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Scalar-List-Utils
BuildRequires:  perl-Carp
BuildRequires:  perl-Exporter
BuildRequires:  perl-generators
Requires:       perl-Carp
Requires:       perl-Exporter

%description
Data::Alias provides aliasing semantics for Perl scalar, array and hash
operations through an XS extension to the Perl interpreter.

%prep
%autosetup -n Data-Alias-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="%{optflags}"
%make_build

%install
%make_install
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license README Alias.xs
%doc Changes
%{perl_vendorarch}/Data/Alias.pm
%{perl_vendorarch}/auto/Data/Alias/
%{_mandir}/man3/Data::Alias.3*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.30-1
- Package the pinned official release and preserve the complete default suite.
