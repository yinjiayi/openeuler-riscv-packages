# SPDX-License-Identifier: Apache-2.0
Name:           perl-Time-Tiny
Version:        1.08
Release:        2%{?dist}
Summary:        Lightweight Perl time object
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Time-Tiny
Source0:        Time-Tiny-%{version}.tar.gz
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
Time::Tiny represents a time of day with hour, minute and second fields,
string conversion, and an optional DateTime conversion method.

%prep
%autosetup -n Time-Tiny-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve both default files. DateTime is an explicit build dependency so
# all seven upstream conversion assertions run rather than self-skip.
%{__perl} -MDateTime -MDateTime::Locale -MDateTime::TimeZone -e 1
if ! %make_build test TEST_VERBOSE=1 > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=2, Tests=16,' upstream-tests.log
grep -q "ok 10 - An object of class 'DateTime' isa 'DateTime'" upstream-tests.log
grep -q '^ok 15 - ->day matches$' upstream-tests.log
if grep -Eiq 'skipped:|# SKIP' upstream-tests.log; then
  echo 'A default upstream test was skipped' >&2
  exit 1
fi

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Time/Tiny.pm
%{_mandir}/man3/Time::Tiny.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.08-2
- Keep all DateTime assertions while expecting the 1.35 C-locale alias.

* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.08-1
- Package the official CPAN release with both default upstream tests.
