# SPDX-License-Identifier: Apache-2.0
Name:           perl-Test-Refcount
Version:        0.10
Release:        1%{?dist}
Summary:        Assert reference counts of Perl objects
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Test-Refcount
Source0:        Test-Refcount-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(Module::Build) >= 0.4004
BuildRequires:  perl(B)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::Builder::Module)
BuildRequires:  perl(Test::Builder::Tester)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl-generators
Requires:       perl(B)
Requires:       perl(Scalar::Util)
Requires:       perl(Test::Builder)
Requires:       perl(Test::Builder::Module)

%description
Test::Refcount supplies assertions for checking the number of references
to Perl objects and diagnosing unexpected retained references.

%prep
%autosetup -n Test-Refcount-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all six default upstream files, including reference-type and POD tests.
./Build test

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Test/Refcount.pm
%{_mandir}/man3/Test::Refcount.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.10-1
- Package official CPAN release with all default tests.
