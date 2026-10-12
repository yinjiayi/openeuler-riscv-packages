# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-BOM
Version:        0.18
Release:        1%{?dist}
Summary:        Perl utilities for handling Unicode byte order marks
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-BOM
Source0:        File-BOM-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Readonly)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)

%description
File::BOM detects Unicode byte order marks and provides decoding, filehandle,
and PerlIO interfaces for text with or without a BOM.

%prep
%autosetup -n File-BOM-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Run all six upstream test files, including fixture setup/teardown and the
# POD checks enabled by the declared Test::Pod dependencies.
./Build test

%files
%doc Changes README README-cygwin TODO
%{perl_vendorlib}/File/BOM.pm
%{_mandir}/man3/File::BOM.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.18-1
- Package the official CPAN release and complete upstream test suite.
