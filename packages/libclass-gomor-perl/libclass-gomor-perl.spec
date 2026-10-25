# SPDX-License-Identifier: Apache-2.0
Name:           perl-Class-Gomor
Version:        1.03
Release:        1%{?dist}
Summary:        Hash- and array-backed Perl class builders
License:        Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Gomor
Source0:        Class-Gomor-%{version}.tar.gz
Patch0:         0001-fix-hash-nested-fullclone.patch

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Pod::Coverage::CountParents)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl-generators
Requires:       perl(Data::Dumper)

%description
Class::Gomor provides hash- and array-backed base classes with generated
accessors and cloning of Class::Gomor objects.

%prep
%autosetup -n Class-Gomor-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all thirteen default upstream files. Only the publisher's Kwalitee
# metadata-quality file may self-skip; both POD files must actually run.
if ! ./Build test > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=13, Tests=16,' upstream-tests.log
for test_file in 01-pod-coverage 01-test-pod 01-use 02-nocheck 03-hash 04-hash-nocheck 04-test-kwalitee 05-array 06-array-nocheck 07-hash-clone 08-hash-fullclone 09-array-clone 10-array-fullclone; do
  grep -Eq "^t/${test_file}\\.t" upstream-tests.log
done
grep -Eq '^t/01-pod-coverage\.t[[:space:].]+ok' upstream-tests.log
grep -Eq '^t/01-test-pod\.t[[:space:].]+ok' upstream-tests.log
grep -Eq '^t/04-test-kwalitee\.t[[:space:].]+skipped: Test::Kwalitee not installed; skipping' upstream-tests.log
if grep -Ei 'skipped:|# SKIP' upstream-tests.log | grep -Ev '^t/04-test-kwalitee\.t[[:space:].]+skipped: Test::Kwalitee not installed; skipping'; then
  echo 'Unexpected default upstream test skip' >&2
  exit 1
fi

%files
%license LICENSE LICENSE.Artistic
%doc README Changes
%{perl_vendorlib}/Class/Gomor.pm
%{perl_vendorlib}/Class/Gomor/Array.pm
%{perl_vendorlib}/Class/Gomor/Hash.pm
%{_mandir}/man3/Class::Gomor*.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.03-1
- Package official CPAN release and fix upstream Hash nested full-clone bug.
