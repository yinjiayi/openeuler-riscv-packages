# SPDX-License-Identifier: Apache-2.0
Name:           perl-sort-naturally
Version:        1.03
Release:        1%{?dist}
Summary:        Sort text lexically and digit runs numerically in Perl
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND GPL-3.0-only
URL:            https://metacpan.org/dist/Sort-Naturally
Source0:        Sort-Naturally-1.03.tar.gz
Source1:        Artistic-1.0-Perl.txt
Source2:        GPL-1.0.txt
Source3:        GPL-3.0.txt
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Config)
BuildRequires:  perl(strict)
BuildRequires:  perl(locale)
BuildRequires:  perl(integer)
BuildRequires:  perl(Test)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Carp)
Requires:       perl
Requires:       perl(Config)
Requires:       perl(strict)
Requires:       perl(locale)
Requires:       perl(integer)
Requires:       perl(Exporter)
Requires:       perl(Carp)

%description
Sort::Naturally compares text lexically while comparing digit runs
numerically, so file2 sorts before file10. It provides sorting and
comparison functions for Perl programs.

%prep
%autosetup -n Sort-Naturally-%{version} -p1
install -pm0644 %{SOURCE1} Artistic-1.0-Perl.txt
install -pm0644 %{SOURCE2} GPL-1.0.txt
install -pm0644 %{SOURCE3} GPL-3.0.txt
cat <<'DONOR_NOTICE' > EUMM-Upgrade-NOTICE
Makefile.PL includes the build-only WriteMakefile1 helper, version 0.21.
Copyright 2009 Alexandr Ciornii.
License: GPL-3.0-only (see GPL-3.0.txt).
Donor: https://cpan.metacpan.org/authors/id/C/CH/CHORNY/App-EUMM-Upgrade-0.21.tar.gz
The helper is not installed as part of the Perl module.
DONOR_NOTICE

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/Sort/Naturally.pm
test -f %{buildroot}%{_mandir}/man3/Sort::Naturally.3pm

%check
make test TEST_VERBOSE=1

%files
%license README Artistic-1.0-Perl.txt GPL-1.0.txt GPL-3.0.txt EUMM-Upgrade-NOTICE
%doc ChangeLog
%{perl_vendorlib}/Sort/Naturally.pm
%{_mandir}/man3/Sort::Naturally.3pm*

%changelog
* Wed Nov 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.03-1
- Package the fixed CPAN release and preserve the original default tests.
