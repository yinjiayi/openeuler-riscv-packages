# SPDX-License-Identifier: Apache-2.0
Name:           perl-Data-Hexdumper
Version:        3.0001
Release:        1%{?dist}
Summary:        Format binary data as readable hexadecimal dumps
License:        GPL-2.0-only OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Hexdumper
Source0:        Data-Hexdumper-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl-generators

%description
Data::Hexdumper renders binary data with configurable output formats,
endianness and word lengths.

%prep
%autosetup -n Data-Hexdumper-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all five upstream t/*.t files, including POD and POD coverage tests.
# Fail rather than accept an optional test silently skipped for missing tools.
%{__perl} -MTest::Pod -MTest::Pod::Coverage -e 1
if ! %make_build test > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
awk '/^Files=5, Tests=/ { n=$2; sub(/^Tests=/, "", n); if (n+0 >= 29) ok=1 } END { exit !ok }' upstream-tests.log
if grep -Eiq 'skipped:|# SKIP' upstream-tests.log; then
  echo 'A default upstream test was skipped' >&2
  exit 1
fi

%files
%license GPL2.txt ARTISTIC.txt
%doc CHANGELOG README
%{perl_vendorlib}/Data/Hexdumper.pm
%{_mandir}/man3/Data::Hexdumper.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0001-1
- Package the official CPAN release with every default upstream test.
