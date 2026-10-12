# SPDX-License-Identifier: Apache-2.0
Name:           perl-List-Rotation-Cycle
Version:        1.009
Release:        1%{?dist}
Summary:        Cycle through lists with a memoized Perl iterator
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/List-Rotation-Cycle
Source0:        List-Rotation-Cycle-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
List::Rotation::Cycle provides a memoized iterator that advances through a
list and wraps back to its first element.

%prep
%autosetup -n List-Rotation-Cycle-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all five default t/*.t files. Upstream t/00.signature.t skips unless
# TEST_SIGNATURE is explicitly set; no signature validation is claimed.
%make_build test

%files
%license lib/List/Rotation/Cycle.pm
%doc Changes README
%{perl_vendorlib}/List/Rotation/Cycle.pm
%{_mandir}/man3/List::Rotation::Cycle.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.009-1
- Package official CPAN release with complete default upstream tests.
