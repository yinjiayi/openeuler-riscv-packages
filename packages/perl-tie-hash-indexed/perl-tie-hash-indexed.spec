# SPDX-License-Identifier: Apache-2.0
Name:           perl-tie-hash-indexed
Version:        0.08
Release:        1%{?dist}
Summary:        Ordered hashes for Perl implemented in XS
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Tie-Hash-Indexed
Source0:        Tie-Hash-Indexed-0.08.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Storable
BuildRequires:  perl-generators
BuildRequires:  findutils


%description
Tie::Hash::Indexed provides insertion-ordered Perl hashes, with tied-hash and
object-oriented interfaces implemented in XS.

%prep
%autosetup -n Tie-Hash-Indexed-%{version}

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
%license README ppport.h
%doc Changes README.md
%{perl_vendorarch}/Tie/Hash/Indexed.pm
%{perl_vendorarch}/auto/Tie/Hash/Indexed/
%{_mandir}/man3/Tie::Hash::Indexed.3*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.08-1
- Package fixed official source with all original tests and license notices.
