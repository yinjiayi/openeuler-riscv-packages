# SPDX-License-Identifier: Apache-2.0
Name:           perl-Devel-SimpleTrace
Version:        0.08
Release:        1%{?dist}
Summary:        Add Perl stack traces to warnings and exceptions
License:        GPL-2.0-only OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Devel-SimpleTrace
Source0:        Devel-SimpleTrace-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::Distribution)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Test::Portability::Files)
BuildRequires:  perl(strict)
BuildRequires:  perl-generators
Requires:       perl(Data::Dumper)
Requires:       perl(strict)

%description
Devel::SimpleTrace extends Perl warnings and exceptions with caller stack
traces to help locate the originating code path.

%prep
%autosetup -n Devel-SimpleTrace-%{version}

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all ten upstream default files. The official target supplies the
# optional distribution, POD, coverage and portability test modules.
if ! ./Build test > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=10, Tests=[1-9][0-9]*,' upstream-tests.log
for name in 00load 00prereq 01basic 02hooks 03showrefs0 03showrefs1 distchk pod podcover portfs; do
  grep -Eq "^t/${name}\\.t[[:space:].]+ok$" upstream-tests.log
done
if grep -Ei '^t/.*skipped:|# SKIP' upstream-tests.log; then
  echo 'An upstream default test skipped unexpectedly' >&2
  exit 1
fi

%files
%license LICENSE LICENSE.Artistic LICENSE.GPL
%doc Changes INSTALL README
%{perl_vendorlib}/Devel/SimpleTrace.pm
%{_mandir}/man3/Devel::SimpleTrace.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.08-1
- Package the official CPAN release and retain its complete default suite.
