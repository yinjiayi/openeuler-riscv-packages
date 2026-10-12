# SPDX-License-Identifier: Apache-2.0
Name:           perl-Date-HolidayParser
Version:        0.43
Release:        1%{?dist}
Summary:        Parse holiday definitions and export iCalendar events
License:        Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Date-HolidayParser
Source0:        Date-HolidayParser-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Moo)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(POSIX)
BuildRequires:  perl-generators
Requires:       perl(Moo)

%description
Date::HolidayParser reads text holiday definitions and resolves holidays by
year. Its iCalendar companion exposes the resulting events and dates.

%prep
%autosetup -n Date-HolidayParser-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# The unmodified third upstream test exercises GMT, CET and EST. Fix the
# inherited timezone so its optional fourth zone cannot change the count.
if ! TZ=GMT %make_build test > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -q '^Files=3, Tests=374,' upstream-tests.log
for name in 01-Date-HolidayParser 02-iCalendar-submod-basics 03-iCalendar; do
  grep -Eq "^t/${name}\\.t[[:space:].]+ok$" upstream-tests.log
done
if grep -Ei '^t/.*skipped:|# SKIP' upstream-tests.log; then
  echo 'An upstream default test skipped unexpectedly' >&2
  exit 1
fi

%files
%license COPYING COPYING.gpl COPYING.artistic
%doc README Changes
%{perl_vendorlib}/Date/HolidayParser.pm
%{perl_vendorlib}/Date/HolidayParser/iCalendar.pm
%{_mandir}/man3/Date::HolidayParser.3*
%{_mandir}/man3/Date::HolidayParser::iCalendar.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.43-1
- Package official CPAN release with all three default upstream tests.
