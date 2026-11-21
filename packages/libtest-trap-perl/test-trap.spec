# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-trap
Version:        0.3.5
Release:        1%{?dist}
Summary:        Trap output and exits from Perl test code
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Test-Trap
Source0:        Test-Trap-v0.3.5.tar.gz
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Data::Dump)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Tester) >= 0.107
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(version)
BuildRequires:  perl(warnings)
BuildRequires:  perl-generators
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(Config)
Requires:       perl(Data::Dump)
Requires:       perl(Exporter)
Requires:       perl(File::Temp)
Requires:       perl(IO::Handle)
Requires:       perl(Test::Builder)
Requires:       perl(Test::More)
Requires:       perl(Test::Tester) >= 0.107
Requires:       perl(base)
Requires:       perl(constant)
Requires:       perl(lib)
Requires:       perl(strict)
Requires:       perl(version)
Requires:       perl(warnings)

%description
Trap output and exits from Perl test code

%prep
%autosetup -n Test-Trap-v%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
./Build test verbose=1

%files
%license README
%doc Changes
%{perl_vendorlib}/Test/Trap.pm
%{perl_vendorlib}/Test/Trap/
%{_mandir}/man3/Test::Trap.3*
%{_mandir}/man3/Test::Trap::Builder*.3*

%changelog
* Tue Nov 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.5-1
- Package the fixed CPAN release and retain its original default tests.
