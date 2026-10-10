# SPDX-License-Identifier: Apache-2.0
Name:           perl-Data-StreamSerializer
Version:        0.07
Release:        1%{?dist}
Summary:        XS serializer for Perl data streams
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Data-StreamSerializer
Source0:        Data-StreamSerializer-%{version}.tar.gz

BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(Sys::Hostname)
BuildRequires:  perl-generators
Requires:       perl(XSLoader)

%description
Data::StreamSerializer incrementally serializes Perl data structures
through an XS implementation.

%prep
%autosetup -n Data-StreamSerializer-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Absolute paths prevent a loader policy from rejecting upstream relative blib paths.
export PERL5LIB="$PWD/blib/lib:$PWD/blib/arch"
%{__perl} -MB -MData::StreamSerializer -e 'die "XS backend inactive\n" unless B::svref_2object(\&Data::StreamSerializer::_next)->XSUB'
if ! %make_build test > upstream-tests.log 2>&1; then
  cat upstream-tests.log
  exit 1
fi
cat upstream-tests.log
grep -q '^Result: PASS$' upstream-tests.log
grep -Eq '^Files=5, Tests=70,' upstream-tests.log
if grep -Eiq 'skipped:|# SKIP' upstream-tests.log; then
  echo 'A default upstream test was skipped' >&2
  exit 1
fi

%files
%license debian/copyright
%doc README Changes
%{perl_vendorarch}/Data/StreamSerializer.pm
%{perl_vendorarch}/auto/Data/StreamSerializer/
%{_mandir}/man3/Data::StreamSerializer.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.07-1
- Package the official CPAN XS release with every default upstream test.
