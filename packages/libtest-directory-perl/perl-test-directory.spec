# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-directory
Version:        0.052
Release:        1%{?dist}
Summary:        Create and verify test directories in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Test-Directory
Source0:        Test-Directory-0.052.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Test::Builder::Module)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  findutils
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::Builder::Tester)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(constant)
BuildRequires:  perl(lib)
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(Fcntl)
Requires:       perl(File::Spec)
Requires:       perl(File::Temp)
Requires:       perl(Test::Builder::Module)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Test::Directory creates temporary test files and directories and checks
whether their contents match the expected test fixture.

%prep
%autosetup -n Test-Directory-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"
find "%{buildroot}" -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license README
%doc Changes
%{perl_vendorlib}/Test/Directory.pm
%{_mandir}/man3/Test::Directory.3*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.052-1
- Package Test::Directory with all original tests and original license.
