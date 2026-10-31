# SPDX-License-Identifier: Apache-2.0
Name:           perl-Time-Piece-MySQL
Version:        0.06
Release:        1%{?dist}
Summary:        MySQL date and time helpers for Time::Piece
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Time-Piece-MySQL
Source0:        Time-Piece-MySQL-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Time::Piece)
BuildRequires:  perl(Time::Seconds)
BuildRequires:  perl(Test::More)
BuildRequires:  perl-generators
Requires:       perl(Time::Piece)
Requires:       perl(Time::Seconds)

%description
Time::Piece::MySQL extends Time::Piece with conversion helpers for MySQL
date, time, datetime and timestamp representations.

%prep
%autosetup -n Time-Piece-MySQL-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain the complete original three-file suite, including date and
# timestamp parsing, and reject any unexpected skip.
if ! %make_build test > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -q '^Files=3, Tests=26,' upstream-tests.log
for name in basic datetime timestamp; do
  grep -Eq "^t/${name}\\.t[[:space:].]+ok$" upstream-tests.log
done
if grep -Ei '^t/.*skipped:|# SKIP' upstream-tests.log; then
  echo 'An upstream default test skipped unexpectedly' >&2
  exit 1
fi

%files
%doc README Changes
%{perl_vendorlib}/Time/Piece/MySQL.pm
%{_mandir}/man3/Time::Piece::MySQL.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.06-1
- Package official CPAN release with all three default upstream tests.
