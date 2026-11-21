# SPDX-License-Identifier: Apache-2.0
Name:           perl-test-exports
Version:        1
Release:        1%{?dist}
Summary:        Test Perl module exports
License:        BSD-2-Clause
URL:            https://metacpan.org/dist/Test-Exports
Source0:        Test-Exports-1.tar.gz
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  sed
BuildRequires:  perl
BuildRequires:  perl(B)
BuildRequires:  perl(Module::Build) >= 0.36
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::Builder::Module)
BuildRequires:  perl(Test::More) >= 0.65
BuildRequires:  perl(Test::Most) >= 0.23
BuildRequires:  perl(Test::Tester) >= 0.08
BuildRequires:  perl(parent)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl-generators
Requires:       perl
Requires:       perl(B)
Requires:       perl(Test::Builder)
Requires:       perl(Test::Builder::Module)
Requires:       perl(parent)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Test Perl module exports

%prep
%autosetup -n Test-Exports-%{version} -p1
# Retain the original copyright, conditions and disclaimer verbatim.
sed -n '/^=head1 COPYRIGHT$/,/^=cut$/p' lib/Test/Exports.pm > LICENSE.upstream

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete

%check
./Build test verbose=1

%files
%license LICENSE.upstream
%doc Changes README
%{perl_vendorlib}/Test/Exports.pm
%{_mandir}/man3/Test::Exports.3*

%changelog
* Tue Nov 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1-1
- Package the fixed CPAN release and retain the original default tests.
