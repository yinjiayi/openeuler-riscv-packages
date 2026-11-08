# SPDX-License-Identifier: Apache-2.0
Name:           libsort-key-top-perl
Version:        0.08
Release:        1%{?dist}
Summary:        Select and sort the top entries of a Perl list
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Sort-Key-Top
Source0:        Sort-Key-Top-%{version}.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(XSLoader)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl
Requires:       perl(XSLoader)
Requires:       perl(Carp)
Requires:       perl(Exporter)

%description
Sort::Key::Top selects the best-ranked entries of a Perl list,
with optional ordering and numeric or string keys. It uses a Perl XS
extension for the selection and sorting routines.

%prep
%autosetup -n Sort-Key-Top-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 OPTIMIZE="%{optflags}"
%make_build
test -s blib/arch/auto/Sort/Key/Top/Top.so

%install
make pure_install DESTDIR=%{buildroot}
install -pm0644 %{SOURCE1} Artistic-1.0-Perl.txt
install -pm0644 %{SOURCE2} GPL-1.0.txt
# Verbatim copyright and license blocks from the SHA-pinned archived headers.
{
    sed -n '328,337p' ppport.h
    printf '\n'
    sed -n '1,9p;36,48p' sort.h
} > BUNDLED-NOTICES.txt

%check
make test TEST_VERBOSE=1

%files
%license README Artistic-1.0-Perl.txt GPL-1.0.txt BUNDLED-NOTICES.txt
%doc Changes
%{perl_vendorarch}/Sort/Key/Top.pm
%{perl_vendorarch}/auto/Sort/Key/Top/
%{_mandir}/man3/Sort::Key::Top.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.08-1
- Package the fixed native XS release and unchanged default tests.
