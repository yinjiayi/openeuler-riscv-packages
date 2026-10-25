# SPDX-License-Identifier: Apache-2.0
Name:           perl-Class-Measure
Version:        0.10
Release:        1%{?dist}
Summary:        Create, compare, and convert units of measurement in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-Measure
Source0:        Class-Measure-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Module::Build::Tiny) >= 0.035
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Sub::Exporter) >= 0.982
BuildRequires:  perl(Test2::V0) >= 0.000094
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl-generators
Requires:       perl(Scalar::Util)
Requires:       perl(Sub::Exporter) >= 0.982

%description
Class::Measure provides an extensible base class for unit conversion and
measurement arithmetic. Class::Measure::Length supplies length units.

%prep
%autosetup -n Class-Measure-%{version}

%build
%{__perl} Build.PL --installdirs vendor
./Build build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run the unchanged four default upstream tests and all 29 assertions.
if ! ./Build test > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=4, Tests=29,' upstream-tests.log
for test_file in conv_via_sub exponential_notation length measure; do
  grep -Eq "^t/${test_file}\\.t" upstream-tests.log
done
if grep -Eiq 'skipped:|# SKIP' upstream-tests.log; then
  echo 'A default upstream test was skipped' >&2
  exit 1
fi

%files
%license LICENSE
%doc README.md Changes
%{perl_vendorlib}/Class/Measure.pm
%{perl_vendorlib}/Class/Measure/Length.pm
%{_mandir}/man3/Class::Measure*.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.10-1
- Package official CPAN release with all four default upstream tests.
