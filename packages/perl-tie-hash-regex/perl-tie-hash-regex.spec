# SPDX-License-Identifier: Apache-2.0
Name:           perl-tie-hash-regex
Version:        2.0.0
Release:        1%{?dist}
Summary:        Perl tied hashes with regular-expression key matching
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Tie-Hash-Regex
Source0:        Tie-Hash-Regex-2.0.0.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-generators
BuildRequires:  findutils


%description
Tie::Hash::Regex implements tied Perl hashes with exact and regular-expression
key matching. It supports both an explicit tie interface and a Regex attribute,
and handles malformed patterns as non-matches.

%prep
%autosetup -n Tie-Hash-Regex-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%make_build test

%files
%license README
%doc Changes
%{perl_vendorlib}/Tie/Hash/Regex.pm
%{_mandir}/man3/Tie::Hash::Regex.3*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.0-1
- Package the fixed official release with all four original default test files.
