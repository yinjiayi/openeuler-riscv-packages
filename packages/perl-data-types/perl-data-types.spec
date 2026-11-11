# SPDX-License-Identifier: Apache-2.0
Name:           perl-Data-Types
Version:        0.17
Release:        1%{?dist}
Summary:        Validate and convert Perl data types
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Types
Source0:        Data-Types-0.17.tar.gz
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl-generators
BuildArch:      noarch
Requires:       perl

%description
Validate and convert Perl data types

%prep
%autosetup -p1 -n Data-Types-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license lib/Data/Types.pm
%doc README.md Changes
%{perl_vendorlib}/Data/Types.pm
%{_mandir}/man3/Data::Types.3*

%changelog
* Thu Oct 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.17-1
- Package Data::Types with its original tests.
