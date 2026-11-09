# SPDX-License-Identifier: Apache-2.0
Name:           libset-crontab-perl
Version:        1.03
Release:        1%{?dist}
Summary:        Expand crontab-style integer lists in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Set-Crontab
Source0:        Set-Crontab-%{version}.tar.gz
Patch0:         0001-correct-original-tap-plan.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Test)
BuildRequires:  perl-Test-Harness
Requires:       perl
Requires:       perl(Carp)

%description
Expand crontab-style integer lists and test membership. Supports ranges,
steps, exclusions, and numeric comparison conditions.

%prep
%setup -q -n Set-Crontab-%{version}
%global _default_patch_fuzz 0
%patch -P 0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
make test
prove -Iblib/lib -Iblib/arch ./test.pl

%files
%license README
%doc Changes
%{perl_vendorlib}/Set/Crontab.pm
%{_mandir}/man3/Set::Crontab.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.03-1
- Package the pinned release and validate all twelve upstream test assertions.
