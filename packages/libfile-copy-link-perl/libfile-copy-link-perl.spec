# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Copy-Link
Version:        0.200
Release:        1%{?dist}
Summary:        Replace symbolic links with copies of their targets
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Copy-Link
Source0:        File-Copy-Link-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-Module-Build
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators

%description
File::Copy::Link replaces a symbolic link with a standalone copy of its
target. File::Spec::Link resolves links; the copylink command exposes the
replacement operation to scripts.

%prep
%autosetup -n File-Copy-Link-%{version} -p1

%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain all nine default t files, including POD and POD coverage.
./Build test

%files
%license README
%doc Changes
%{_bindir}/copylink
%{perl_vendorlib}/File/Copy/Link.pm
%{perl_vendorlib}/File/Spec/Link.pm
%{_mandir}/man1/copylink.1*
%{_mandir}/man3/File::Copy::Link.3*
%{_mandir}/man3/File::Spec::Link.3*

%changelog
* Wed Sep 30 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.200-1
- Package official CPAN release with command, both modules and all tests.
