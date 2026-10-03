# SPDX-License-Identifier: Apache-2.0
Name:           perl-Time-Period
Version:        1.25
Release:        2%{?dist}
Summary:        Test whether a time belongs to a named period
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Time-Period
Source0:        Time-Period-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
BuildRequires:  perl-generators
Requires:       perl(Exporter)

%description
Time::Period checks whether a timestamp falls within a named period,
including weekday, year, month, day, hour, minute and second ranges.

%prep
%autosetup -n Time-Period-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep the unchanged ten-file, 213-assertion default upstream suite.
if ! %make_build test > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=10, Tests=213,' upstream-tests.log
for test_file in 01_time_period 02_weekday 03_year 04_month 05_week 06_year_day 07_month_day 08_hour 09_minute 10_second; do
  grep -Eq "^t/${test_file}\\.t" upstream-tests.log
done
if grep -Eiq 'skipped:|# SKIP' upstream-tests.log; then
  echo 'A default upstream test was skipped' >&2
  exit 1
fi

%files
%license LICENSE
%doc README
%{perl_vendorlib}/Time/Period.pm
%{_mandir}/man3/Time::Period.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.25-2
- List only the README document present in the official release archive.

* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.25-1
- Package official CPAN release with all ten default upstream tests.
