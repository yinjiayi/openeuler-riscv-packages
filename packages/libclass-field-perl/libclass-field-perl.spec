# SPDX-License-Identifier: Apache-2.0
Name:           perl-Class-Field
Version:        0.24
Release:        1%{?dist}
Summary:        Perl class field accessor generator
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Field
Source0:        Class-Field-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Encode)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
BuildRequires:  perl-generators
Requires:       perl(Data::Dumper)
Requires:       perl(Encode)
Requires:       perl(Scalar::Util)

%description
Class::Field generates Perl object field accessors and constant methods.

%prep
%autosetup -n Class-Field-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all five default files. The author-only POD file self-skips unless
# AUTHOR_TESTING is set; all four functional files must run 15 assertions.
if ! %make_build test TEST_VERBOSE=1 > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=5, Tests=15,' upstream-tests.log
grep -Eq '^t/000-compile-modules\.t' upstream-tests.log
grep -Eq '^t/anon\.t' upstream-tests.log
grep -Eq '^t/const\.t' upstream-tests.log
grep -Eq '^t/field\.t' upstream-tests.log
grep -Eq 't/author-pod-syntax\.t.*skipped: these tests are for testing by the author' upstream-tests.log
if grep -E 't/(000-compile-modules|anon|const|field)\.t.*skipped|# SKIP' upstream-tests.log; then
  echo 'A functional upstream test was skipped' >&2
  exit 1
fi

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Class/Field.pm
%{perl_vendorlib}/Class/Field.pod
%{_mandir}/man3/Class::Field.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.24-1
- Package official CPAN release with all default functional upstream tests.
