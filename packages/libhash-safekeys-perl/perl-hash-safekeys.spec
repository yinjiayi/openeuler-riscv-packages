# SPDX-License-Identifier: Apache-2.0
Name:           perl-hash-safekeys
Version:        0.04
Release:        1%{?dist}
Summary:        List Perl hash keys and values without resetting the iterator
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Hash-SafeKeys
Source0:        Hash-SafeKeys-0.04.tar.gz
BuildRequires:  perl
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(base)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(DynaLoader)
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  perl-devel
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::ParseXS)
BuildRequires:  perl(Test::More)
BuildRequires:  findutils
Requires:       perl
Requires:       perl(strict)
Requires:       perl(warnings)
Requires:       perl(base)
Requires:       perl(Exporter)
Requires:       perl(DynaLoader)

%description
Hash::SafeKeys provides XS helpers to read or copy a hash without resetting
its Perl iterator.

%prep
%autosetup -n Hash-SafeKeys-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="%{optflags}"
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete
find "%{buildroot}" -type f -name '*.bs' -size 0 -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license README
%doc Changes
%{perl_vendorarch}/Hash/SafeKeys.pm
%{perl_vendorarch}/auto/Hash/SafeKeys/
%{_mandir}/man3/Hash::SafeKeys.3*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.04-1
- Package Hash::SafeKeys 0.04 and retain its full original tests.
