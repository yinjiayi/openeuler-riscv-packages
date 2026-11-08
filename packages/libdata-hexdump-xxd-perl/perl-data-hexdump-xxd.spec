# SPDX-License-Identifier: Apache-2.0
Name:           perl-data-hexdump-xxd
Version:        0.1.1
Release:        1%{?dist}
Summary:        Format and reverse xxd-style hexadecimal dumps in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-HexDump-XXD
Source0:        Data-HexDump-XXD-0.1.1.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(version)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(Carp)
BuildRequires:  perl(base)
BuildRequires:  perl(Exporter)
BuildRequires:  make
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More)
Requires:       perl
Requires:       perl(version)
Requires:       perl(strict)
Requires:       perl(warnings)
Requires:       perl(Carp)
Requires:       perl(base)
Requires:       perl(Exporter)

%description
Data::HexDump::XXD formats byte strings as xxd-style hexadecimal dumps
and converts those dumps back to their original bytes.

%prep
%autosetup -n Data-HexDump-XXD-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license README
%doc Changes
%{perl_vendorlib}/Data/HexDump/XXD.pm
%{_mandir}/man3/Data::HexDump::XXD.3*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.1-1
- Package Data::HexDump::XXD 0.1.1 with its original default tests.
