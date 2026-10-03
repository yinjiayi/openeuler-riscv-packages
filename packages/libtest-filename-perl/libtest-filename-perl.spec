# SPDX-License-Identifier: Apache-2.0
Name:           perl-Test-Filename
Version:        0.03
Release:        1%{?dist}
Summary:        Portable filename comparison for Perl tests
License:        Apache-2.0
URL:            https://metacpan.org/dist/Test-Filename
Source0:        Test-Filename-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Path::Tiny)
BuildRequires:  perl(Test::Builder::Module)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Tester)
BuildRequires:  perl-generators
Requires:       perl(Path::Tiny)
Requires:       perl(Test::Builder::Module)

%description
Test::Filename compares pathnames in Perl tests after normalizing their
platform-specific filename syntax.

%prep
%autosetup -n Test-Filename-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run both original default files, including the negative filename cases.
%make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Test/Filename.pm
%{_mandir}/man3/Test::Filename.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.03-1
- Package official CPAN release with both default tests.
