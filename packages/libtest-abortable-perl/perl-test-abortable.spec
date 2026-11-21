# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-abortable
Version:        0.003
Release:        1%{?dist}
Summary:        Catch selected exceptions inside Perl test subtests
License:        (GPL-1.0-or-later OR Artistic-1.0-Perl) AND Apache-2.0
URL:            https://metacpan.org/dist/Test-Abortable
Source0:        Test-Abortable-0.003.tar.gz
Patch0:         0001-preserve-helper-notices.patch
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(Sub::Exporter)
BuildRequires:  perl(Test2::API) >= 1.302075
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  make
BuildRequires:  findutils
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Needs)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(CPAN::Meta)
BuildRequires:  tar
BuildRequires:  gzip
Requires:       perl
Requires:       perl(Sub::Exporter)
Requires:       perl(Test2::API) >= 1.302075
Requires:       perl(overload)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Test::Abortable wraps Perl subtests and blocks so that explicitly abortable
exceptions can emit their test events while ordinary errors still propagate.

%prep
%autosetup -n Test-Abortable-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%{__make} pure_install DESTDIR="%{buildroot}"

%check
%{__make} test TEST_VERBOSE=1

%files
%license LICENSE GENERATED-HELPER-NOTICES GENERATED-HELPER-APACHE-LICENSE
%doc README Changes
%{perl_vendorlib}/Test/Abortable.pm
%{_mandir}/man3/Test::Abortable.3*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.003-1
- Package Test::Abortable 0.003 with unchanged tests and complete helper notices.
