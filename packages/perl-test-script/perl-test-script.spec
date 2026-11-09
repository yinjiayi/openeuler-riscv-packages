# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-script
Version:        1.31
Release:        1%{?dist}
Summary:        Basic cross-platform tests for Perl scripts
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Test-Script
Source0:        https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/Test-Script-%{version}.tar.gz
Patch0:         0001-preserve-generated-template-notices.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl(Capture::Tiny)
BuildRequires:  perl(File::Spec) >= 0.80
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Probe::Perl) >= 0.01
BuildRequires:  perl(Test2::API) >= 1.302015
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  perl(Test2::V0) >= 0.000121
Requires:       perl
Requires:       perl(Capture::Tiny)
Requires:       perl(File::Spec) >= 0.80
Requires:       perl(IO::Handle)
Requires:       perl(Probe::Perl) >= 0.01
Requires:       perl(Test2::API) >= 1.302015
Requires:       perl(Text::ParseWords)

%description
Test Perl scripts for compilation, execution, exit status, and captured
standard output and error without depending on the caller's shell.

%prep
%setup -q -n Test-Script-%{version}
%patch -P 0 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR="%{buildroot}"

%check
make test

%files
%license LICENSE GENERATED-TEMPLATE-NOTICES
%doc README Changes
%{perl_vendorlib}/Test/Script.pm
%{_mandir}/man3/Test::Script.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.31-1
- Package fixed official release, original default tests and generated notices.
