# SPDX-License-Identifier: Apache-2.0
Name:           perl-Class-Trigger
Version:        0.15
Release:        1%{?dist}
Summary:        Inheritable callbacks for Perl classes
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Trigger
Source0:        Class-Trigger-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.59
BuildRequires:  perl(IO::Scalar)
BuildRequires:  perl(IO::WrapTie)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More) >= 0.32
BuildRequires:  perl(Test::Pod) >= 1.41
BuildRequires:  perl-generators
Requires:       perl(Carp)

%description
Class::Trigger adds inheritable named callbacks to Perl classes and
objects, including abortable callbacks and trigger result inspection.

%prep
%autosetup -n Class-Trigger-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run every unchanged default file, including the author POD syntax test.
# AUTHOR_TESTING activates that upstream self-skipped file without altering it.
if ! AUTHOR_TESTING=1 %make_build test TEST_VERBOSE=1 > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=11, Tests=52,' upstream-tests.log
for test_file in 00_compile 01_trigger 02_valid 03_inherit 04_object 05_args 06_coverage 07_abortable_callbacks 08_dollar_underscore 09_inherit author-pod-syntax; do
  grep -Eq "^t/${test_file}\\.t" upstream-tests.log
done
if grep -Eiq 'skipped:|# SKIP' upstream-tests.log; then
  echo 'A default upstream test was skipped' >&2
  exit 1
fi

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Class/Trigger.pm
%{_mandir}/man3/Class::Trigger.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.15-1
- Package official CPAN release and run all eleven default upstream tests.
