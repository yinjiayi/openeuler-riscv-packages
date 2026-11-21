# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-nobreakpoints
Version:        0.17
Release:        1%{?dist}
Summary:        Check Perl source files for debugger breakpoints
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Test-NoBreakpoints
Source0:        Test-NoBreakpoints-0.17.tar.gz
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.52
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::More) >= 0.92
BuildRequires:  perl(Test::NoWarnings)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Tester) >= 0.09
BuildRequires:  perl(Test::UseAllModules)
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
BuildRequires:  perl-generators
Requires:       perl
Requires:       perl(Exporter)
Requires:       perl(File::Find)
Requires:       perl(File::Spec)
Requires:       perl(Test::Builder)
Requires:       perl(strict)
Requires:       perl(vars)

%description
Check Perl source files for debugger breakpoints

%prep
%autosetup -n Test-NoBreakpoints-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/Test/NoBreakpoints.pm
%{_mandir}/man3/Test::NoBreakpoints.3*

%changelog
* Tue Nov 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.17-1
- Package the fixed official source with its unchanged default test suite.
