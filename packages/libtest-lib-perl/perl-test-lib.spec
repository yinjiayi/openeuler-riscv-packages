# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-lib
Version:        0.003
Release:        1%{?dist}
Summary:        Use private Perl libraries from a t/lib directory
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Test-Lib
Source0:        Test-Lib-0.003.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  findutils
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More)
Requires:       perl
Requires:       perl(Cwd)
Requires:       perl(File::Spec)
Requires:       perl(lib)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Test::Lib locates a private t/lib directory relative to the calling test
file and adds it to Perl's library search path.

%prep
%autosetup -n Test-Lib-%{version} -p1

%build
# The verified release already provides META.yml. Fail rather than enter
# the upstream maintainer-only Distar bootstrap path.
test -s META.yml
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete
# A case-folding filesystem can make MakeMaker see lib and Lib twice.
find "%{buildroot}%{_mandir}/man3" -type f -name 'Test::Lib::Test::Lib.3*' -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Test/Lib.pm
%{_mandir}/man3/Test::Lib.3*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.003-1
- Package Test::Lib with unchanged recursive tests and original license.
