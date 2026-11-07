# SPDX-License-Identifier: Apache-2.0
Name:           perl-tie-cphash
Version:        2.000
Release:        1%{?dist}
Summary:        Case-preserving case-insensitive hashes for Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Tie-CPHash
Source0:        Tie-CPHash-2.000.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Carp
BuildRequires:  perl-generators
BuildRequires:  findutils
Requires:       perl-Carp


%description
Tie::CPHash implements case-insensitive Perl hashes while retaining the most
recent spelling of each key. It provides the standard tied-hash interface and
additional methods for retrieving original key spellings and adding entries.

%prep
%autosetup -n Tie-CPHash-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Tie/CPHash.pm
%{_mandir}/man3/Tie::CPHash.3*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.000-1
- Package unchanged official release with the complete original default tests.
