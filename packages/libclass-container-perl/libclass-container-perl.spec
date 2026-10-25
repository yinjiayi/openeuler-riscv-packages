# SPDX-License-Identifier: Apache-2.0
Name:           perl-Class-Container
Version:        0.13
Release:        1%{?dist}
Summary:        Glue object frameworks together transparently
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Container
Source0:        Class-Container-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(B::Deparse)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Module::Build) >= 0.3601
BuildRequires:  perl(Params::Validate)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl-generators
Requires:       perl(B::Deparse)
Requires:       perl(Params::Validate)
Requires:       perl(Scalar::Util)

%description
Class::Container provides object containment, delayed construction, and
decoration helpers for Perl class hierarchies.

%prep
%autosetup -n Class-Container-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all three default files. The author-only critic file self-skips unless
# AUTHOR_TESTING is set; both functional files must run all 92 assertions.
if ! %make_build test TEST_VERBOSE=1 > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=3, Tests=92,' upstream-tests.log
grep -Eq '^t/01-basic\.t[[:space:].]*' upstream-tests.log
grep -Eq '^t/02-decorator\.t[[:space:].]*' upstream-tests.log
grep -Eq 't/author-critic\.t.*skipped: these tests are for testing by the author' upstream-tests.log
if grep -E 't/(01-basic|02-decorator)\.t.*skipped|# SKIP' upstream-tests.log; then
  echo 'A functional upstream test was skipped' >&2
  exit 1
fi

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Class/Container.pm
%{_mandir}/man3/Class::Container.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.13-1
- Package official CPAN release and retain all default upstream tests.
