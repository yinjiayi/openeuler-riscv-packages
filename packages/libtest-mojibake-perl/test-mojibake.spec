# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-mojibake
Version:        1.3
Release:        1%{?dist}
Summary:        Check Perl source for character encoding errors
License:        Artistic-1.0-Perl OR GPL-1.0-or-later
URL:            https://metacpan.org/dist/Test-Mojibake
Source0:        Test-Mojibake-1.3.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl >= 5.6.0
BuildRequires:  perl(Encode)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Pod::Usage)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::Builder::Tester)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(blib) >= 1.01
BuildRequires:  perl(bytes)
BuildRequires:  perl(integer)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl-generators
Requires:       perl >= 5.6.0
Requires:       perl(File::Spec::Functions)
Requires:       perl(Pod::Usage)
Requires:       perl(Test::Builder)
Requires:       perl(bytes)
Requires:       perl(integer)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Check Perl source for character encoding errors

%prep
%autosetup -n Test-Mojibake-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE
%doc Changes README
%{_bindir}/scan_mojibake
%{perl_vendorlib}/Test/Mojibake.pm
%{_mandir}/man1/scan_mojibake.1*
%{_mandir}/man3/Test::Mojibake.3*

%changelog
* Tue Nov 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3-1
- Package the fixed CPAN release and retain the original default tests.
