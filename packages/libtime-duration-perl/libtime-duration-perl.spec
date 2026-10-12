# SPDX-License-Identifier: Apache-2.0
Name:           perl-Time-Duration
Version:        1.21
Release:        1%{?dist}
Summary:        Express time durations in English
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Time-Duration
Source0:        Time-Duration-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(constant)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl-generators
Requires:       perl(Exporter)
Requires:       perl(constant)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Time::Duration renders rounded or exact time intervals in English,
including relative phrases such as "ago" and "from now".

%prep
%autosetup -n Time-Duration-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all four default upstream files. Release-only POD checks self-skip;
# both functional files and all 250 assertions must execute without a skip.
if ! %make_build test > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=4, Tests=250,' upstream-tests.log
grep -Eq '^t/01_tdur\.t[[:space:].]+ok' upstream-tests.log
grep -Eq '^t/04_tdur_ms\.t[[:space:].]+ok' upstream-tests.log
grep -Eq '^t/release-02_pod\.t[[:space:].]+skipped: these tests are for release candidate testing$' upstream-tests.log
grep -Eq '^t/release-03_pod_cover\.t[[:space:].]+skipped: these tests are for release candidate testing$' upstream-tests.log
test "$(grep -Ec '^t/.*skipped:' upstream-tests.log)" -eq 2
if grep -Eq '# SKIP|# skip' upstream-tests.log; then
  echo 'An upstream assertion was skipped unexpectedly' >&2
  exit 1
fi

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Time/Duration.pm
%{_mandir}/man3/Time::Duration.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.21-1
- Package official CPAN release and preserve its complete default test suite.
