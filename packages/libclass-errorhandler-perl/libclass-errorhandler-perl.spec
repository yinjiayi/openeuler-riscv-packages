# SPDX-License-Identifier: Apache-2.0
Name:           perl-Class-ErrorHandler
Version:        0.04
Release:        1%{?dist}
Summary:        Base class for Perl error handling
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-ErrorHandler
Source0:        Class-ErrorHandler-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test)
BuildRequires:  perl(base)
BuildRequires:  perl-generators

%description
Class::ErrorHandler supplies class-level and object-level methods for
recording and retrieving error messages in derived Perl classes.

%prep
%autosetup -n Class-ErrorHandler-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run both unchanged default test files and require every assertion.
if ! %make_build test > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=2, Tests=10,' upstream-tests.log
if grep -Eiq 'skipped:|# SKIP' upstream-tests.log; then
  echo 'A default upstream test was skipped' >&2
  exit 1
fi

%files
%license LICENSE
%doc README.md Changes
%{perl_vendorlib}/Class/ErrorHandler.pm
%{_mandir}/man3/Class::ErrorHandler.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.04-1
- Package the official CPAN release with every default upstream test.
