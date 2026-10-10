# SPDX-License-Identifier: Apache-2.0
Name:           perl-Data-Peek
Version:        0.54
Release:        1%{?dist}
Summary:        Low-level Perl debugging and inspection functions
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-Peek
Source0:        Data-Peek-%{version}.tgz

BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl(B)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Perl::Tidy)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Test::Warnings)
BuildRequires:  perl(XSLoader)
BuildRequires:  perl-generators
Requires:       perl(Data::Dumper)
Requires:       perl(XSLoader)

%description
Data::Peek provides low-level XS inspection and debugging functions for
Perl values, alongside formatting helpers.

%prep
%autosetup -n Data-Peek-%{version} -p1

%build
# Upstream's automated mode avoids only the interactive optional DP alias.
# The release contains no xt/ directory and still runs all default t/*.t.
AUTOMATED_TESTING=1 %{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Prove that the built native entry point, POD coverage provider, and
# Perl::Tidy branch are available before unchanged upstream tests run.
export PERL5LIB="$PWD/blib/lib:$PWD/blib/arch"
%{__perl} -MB -MData::Peek -MPerl::Tidy -MTest::Pod::Coverage -e 'die "DPeek XS unavailable\n" unless B::svref_2object(Data::Peek->can("DPeek"))->XSUB; my $out = Data::Peek::DPeek("sample"); die "DPeek unavailable\n" if $out =~ /^Your perl did not/ || $out !~ /sample/'
if ! %make_build test > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
awk '/^Files=15, Tests=/ { n=$2; sub(/^Tests=/, "", n); if (n+0 >= 272) ok=1 } END { exit !ok }' upstream-tests.log
if grep -Eiq 'skipped:|# SKIP|A usable Perl::Tidy is not available' upstream-tests.log; then
  echo 'A default upstream test or Perl::Tidy branch was skipped' >&2
  exit 1
fi

%files
%doc ChangeLog README
%{perl_vendorarch}/Data/Peek.pm
%{perl_vendorarch}/auto/Data/Peek/
%{_mandir}/man3/Data::Peek.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.54-1
- Package the official CPAN release with its native XS and full default tests.
