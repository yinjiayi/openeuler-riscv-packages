# SPDX-License-Identifier: Apache-2.0
Name:           libsort-maker-perl
Version:        0.06
Release:        1%{?dist}
Summary:        Generate reusable Perl sorting routines from key definitions
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Sort-Maker
Source0:        Sort-Maker-0.06.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(base)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(B::Deparse)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Benchmark)
BuildRequires:  perl(vars)
BuildRequires:  perl(lib)
BuildRequires:  perl(List::Util)
Requires:       perl
Requires:       perl(strict)
Requires:       perl(warnings)
Requires:       perl(base)
Requires:       perl(Exporter)
Requires:       perl(Data::Dumper)
Requires:       perl(B::Deparse)
Requires:       perl(List::Util)

%description
Generate reusable Perl sorting routines from key definitions

%prep
%autosetup -n Sort-Maker-%{version} -p1
cp -p %{SOURCE1} %{SOURCE2} .

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/Sort/Maker.pm
test -f %{buildroot}%{_mandir}/man3/Sort::Maker.3pm

%check
make test TEST_VERBOSE=1

%files
%license README Artistic-1.0-Perl.txt GPL-1.0.txt
%doc Changes
%{perl_vendorlib}/Sort/Maker.pm
%{_mandir}/man3/Sort::Maker.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.06-1
- Package the original sorting module and its complete default test suite.
