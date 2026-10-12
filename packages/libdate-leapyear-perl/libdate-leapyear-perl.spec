# SPDX-License-Identifier: Apache-2.0
Name:           perl-Date-Leapyear
Version:        1.72
Release:        1%{?dist}
Summary:        Determine whether a year is a leap year
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Date-Leapyear
Source0:        Date-Leapyear-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl-generators
Requires:       perl(Exporter)

%description
Date::Leapyear exports isleap, which identifies Gregorian leap years.

%prep
%autosetup -n Date-Leapyear-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all three unmodified default files and their fixed year tables.
if ! %make_build test TEST_VERBOSE=1 > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=3, Tests=764,' upstream-tests.log
if grep -Eiq 'skipped:|# SKIP' upstream-tests.log; then
  echo 'A default upstream test was skipped' >&2
  exit 1
fi

%files
%license LICENSE
%doc README
%{perl_vendorlib}/Date/Leapyear.pm
%{_mandir}/man3/Date::Leapyear.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.72-1
- Package the official CPAN release with all default upstream tests.
