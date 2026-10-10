# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-SearchPath
Version:        0.07
Release:        1%{?dist}
Summary:        Perl module for locating files in path-like variables
License:        GPL-2.0-or-later
URL:            https://metacpan.org/dist/File-SearchPath
Source0:        File-SearchPath-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(Module::Build) >= 0.36
BuildRequires:  perl(Test::More)

%description
File::SearchPath searches path-like environment variables for files,
executables, and directories.

%prep
%autosetup -n File-SearchPath-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# The complete upstream default suite is one file with 16 assertions.
./Build test

%files
%doc ChangeLog README
%{perl_vendorlib}/File/SearchPath.pm
%{_mandir}/man3/File::SearchPath.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.07-1
- Package the official CPAN release and full upstream test suite.
