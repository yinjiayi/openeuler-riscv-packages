# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-synopsis
Version:        0.18
Release:        1%{?dist}
Summary:        Test Perl code examples in POD SYNOPSIS sections
License:        Artistic-1.0-Perl OR GPL-1.0-or-later
URL:            https://metacpan.org/dist/Test-Synopsis
Source0:        Test-Synopsis-0.18.tar.gz
BuildArch:      noarch
BuildRequires:  perl >= 5.8.1
BuildRequires:  perl(ExtUtils::Manifest)
BuildRequires:  perl(Pod::Simple) >= 3.09
BuildRequires:  perl(Test::Builder::Module)
BuildRequires:  perl(parent)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(Test::Builder) >= 0.34
BuildRequires:  perl(Test::Builder::Tester)
BuildRequires:  perl(Test::More)
Requires:       perl >= 5.8.1
Requires:       perl(ExtUtils::Manifest)
Requires:       perl(Pod::Simple) >= 3.09
Requires:       perl(Test::Builder::Module)
Requires:       perl(parent)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Test Perl code examples in POD SYNOPSIS sections

%prep
%autosetup -n Test-Synopsis-%{version} -p1

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
%doc Changes README README.md
%{perl_vendorlib}/Test/Synopsis.pm
%{_mandir}/man3/Test::Synopsis.3*

%changelog
* Tue Nov 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.18-1
- Package the fixed CPAN release and retain the original default tests.
