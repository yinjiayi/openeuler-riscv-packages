# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-consistentversion
Version:        0.3.1
Release:        1%{?dist}
Summary:        Test that Perl distribution versions are consistent
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Test-ConsistentVersion
Source0:        Test-ConsistentVersion-v0.3.1.tar.gz
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  perl
BuildRequires:  perl(Carp)
BuildRequires:  perl(English)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Module::Build) >= 0.42
BuildRequires:  perl(Test::Builder) >= 0.94
BuildRequires:  perl(Test::Builder::Tester)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(autodie)
BuildRequires:  perl(strict)
BuildRequires:  perl(version)
BuildRequires:  perl(warnings)
BuildRequires:  perl-generators
Requires:       perl
Requires:       perl(Carp)
Requires:       perl(Test::Builder) >= 0.94
Requires:       perl(autodie)
Requires:       perl(strict)
Requires:       perl(version)
Requires:       perl(warnings)

%description
Test that Perl distribution versions are consistent

%prep
%autosetup -n Test-ConsistentVersion-v%{version} -p1

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
%{perl_vendorlib}/Test/ConsistentVersion.pm
%{_mandir}/man3/Test::ConsistentVersion.3*

%changelog
* Tue Nov 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.1-1
- Package the fixed CPAN release and retain original default tests.
