# SPDX-License-Identifier: Apache-2.0
Name:           perl-tie-hash-readonlystack
Version:        0.2
Release:        1%{?dist}
Summary:        Overlay a read-only Perl hash with override and fallback lookups
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Tie-Hash-ReadonlyStack
Source0:        Tie-Hash-ReadonlyStack-0.2.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  make
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Pod::Coverage)
BuildRequires:  findutils
Requires:       perl
Requires:       perl(strict)
Requires:       perl(Test::More)

%description
Tie::Hash::ReadonlyStack overlays a tied read-only hash with optional lookup
overrides and fallback hashes without mutating the underlying hash.

%prep
%autosetup -n Tie-Hash-ReadonlyStack-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license README
%doc Changes
%{perl_vendorlib}/Tie/Hash/ReadonlyStack.pm
%{perl_vendorlib}/Tie/Hash/ReadonlyStack.pod
%{_mandir}/man3/Tie::Hash::ReadonlyStack.3*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2-1
- Package Tie::Hash::ReadonlyStack with the original tests and author notices.
