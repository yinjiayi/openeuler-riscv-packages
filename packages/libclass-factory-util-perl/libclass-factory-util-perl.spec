# SPDX-License-Identifier: Apache-2.0
Name:           perl-Class-Factory-Util
Version:        1.7
Release:        1%{?dist}
Summary:        Discover subclasses for Perl factory classes
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Factory-Util
Source0:        Class-Factory-Util-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl-generators
Requires:       perl(Carp)

%description
Class::Factory::Util adds a subclasses method that discovers available
factory-class implementations from the Perl module search path.

%prep
%autosetup -n Class-Factory-Util-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all three unchanged default files, including real POD coverage.
%{__perl} -MTest::Pod -MTest::Pod::Coverage -e 'Test::Pod::Coverage->VERSION("1.04")'
if ! ./Build test > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=3, Tests=7,' upstream-tests.log
grep -Eq '^t/pod-coverage\.t[[:space:].]+ok$' upstream-tests.log
if grep -Eiq 'skipped:|# SKIP' upstream-tests.log; then
  echo 'A default upstream test was skipped' >&2
  exit 1
fi

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Class/Factory/Util.pm
%{_mandir}/man3/Class::Factory::Util.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.7-1
- Package the official CPAN release with every default upstream test.
