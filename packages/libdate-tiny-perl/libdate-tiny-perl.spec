# SPDX-License-Identifier: Apache-2.0
Name:           perl-Date-Tiny
Version:        1.07
Release:        1%{?dist}
Summary:        Lightweight Perl date object
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Date-Tiny
Source0:        Date-Tiny-%{version}.tar.gz
Patch0:         0001-test-accept-datetime-locale-135-c-alias.patch

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  perl(DateTime)
BuildRequires:  perl(DateTime::Locale)
BuildRequires:  perl(DateTime::TimeZone)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.17
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::More)
BuildRequires:  perl-generators
Requires:       perl(Carp)
Requires:       perl(overload)

%description
Date::Tiny represents a date with year, month and day fields, string
conversion, and an optional DateTime conversion method.

%prep
%autosetup -n Date-Tiny-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve both default files. DateTime is a hard build dependency so all
# seven original conversion assertions run rather than self-skip.
%{__perl} -MDateTime -MDateTime::Locale -MDateTime::TimeZone -e 1
if ! %make_build test TEST_VERBOSE=1 > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=2, Tests=20,' upstream-tests.log
grep -q '^ok 10 - ->locale ok$' upstream-tests.log
grep -q '^ok 15 - ->day matches$' upstream-tests.log
if grep -Eiq 'skipped:|# SKIP' upstream-tests.log; then
  echo 'A default upstream test was skipped' >&2
  exit 1
fi

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Date/Tiny.pm
%{_mandir}/man3/Date::Tiny.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.07-1
- Package the official CPAN release with both default upstream tests.
