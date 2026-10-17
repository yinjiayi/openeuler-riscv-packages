# SPDX-License-Identifier: Apache-2.0
Name:           perl-Class-WhiteHole
Version:        0.04
Release:        1%{?dist}
Summary:        Reject accidental inheritance of Perl AUTOLOAD methods
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Class-WhiteHole
Source0:        Class-WhiteHole-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Harness
BuildRequires:  perl-generators

%description
Class::WhiteHole prevents accidental AUTOLOAD inheritance and raises ordinary
Perl missing-method errors while preserving static methods and destruction.

%prep
%autosetup -n Class-WhiteHole-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install pure_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep the full original test and line57 error-message fixture unchanged.
%make_build test
# Legacy ok() only prints TAP; Harness makes any notok fail this build.
PERL5LIB="$PWD/blib/lib:$PWD/blib/arch" %{__perl} -MTest::Harness -e 'runtests("t/WhiteHole.t")'

%files
%license lib/Class/WhiteHole.pm
%doc Changes
%{perl_vendorlib}/Class/WhiteHole.pm
%{_mandir}/man3/Class::WhiteHole.3*

%changelog
* Sun Oct 04 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.04-1
- Package official source with complete default TAP tests and installed smoke.
