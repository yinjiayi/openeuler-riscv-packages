# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-SimpleTable
Version:        2.07
Release:        1%{?dist}
Summary:        Create simple ASCII and Unicode tables
License:        Artistic-2.0
URL:            https://metacpan.org/dist/Text-SimpleTable
Source0:        Text-SimpleTable-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl(Unicode::GCString)
BuildRequires:  perl(MIME::Charset)
BuildRequires:  perl-generators
Requires:       perl(Unicode::GCString)
Requires:       perl(MIME::Charset)

%description
Text::SimpleTable formats ASCII tables and, with Unicode::GCString,
supports width-aware Unicode text.

%prep
%autosetup -n Text-SimpleTable-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep all five original tests. Enable both upstream developer POD suites;
# Unicode::GCString and MIME::Charset make the CJK suite runnable on target.
TEST_POD=1 %make_build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Text/SimpleTable.pm
%{_mandir}/man3/Text::SimpleTable.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.07-1
- Package official CPAN release with all five original test files.
