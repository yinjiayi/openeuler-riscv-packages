# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-is
Version:        20140823.1
Release:        1%{?dist}
Summary:        Declarative Perl test context checks
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/DOLMEN/Test-Is-20140823.1
Source0:        Test-Is-%{version}.tar.gz
Source1:        Dist-Zilla-5.020.LICENSE
Source2:        Dist-Zilla-Plugin-Test-Compile-2.043.LICENSE
Source3:        Dist-Zilla-Plugin-ReportVersions-Tiny-1.10.LICENSE
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl >= 5
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(TAP::Formatter::File)
BuildRequires:  perl(TAP::Harness)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
Requires:       perl(Test::More) >= 0.88

%description
Test::Is provides declarative environment and Perl-version conditions
for tests, including the Lancaster Consensus interactive and extended flags.

%prep
%autosetup -n Test-Is-%{version} -p1
mkdir -p vendor-licenses
install -pm0644 %{SOURCE1} vendor-licenses/Dist-Zilla-5.020.LICENSE
install -pm0644 %{SOURCE2} vendor-licenses/Dist-Zilla-Plugin-Test-Compile-2.043.LICENSE
install -pm0644 %{SOURCE3} vendor-licenses/Dist-Zilla-Plugin-ReportVersions-Tiny-1.10.LICENSE

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
make test TEST_VERBOSE=1

%files
%license LICENSE vendor-licenses/*
%doc README Changes
%{perl_vendorlib}/Test/Is.pm
%{_mandir}/man3/Test::Is.3pm*

%changelog
* Wed Nov 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 20140823.1-1
- Package the fixed CPAN release with its original test harness and template terms.
