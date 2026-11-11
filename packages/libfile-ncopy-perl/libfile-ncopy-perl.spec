# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-NCopy
Version:        0.36
Release:        1%{?dist}
Summary:        Perl extension for copying files
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-NCopy
Source0:        File-NCopy-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl(Test::Pod) >= 1.14
BuildRequires:  perl-generators

%description
File::NCopy is a deprecated compatibility module for copying files.

%prep
%autosetup -n File-NCopy-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# The upstream copy test scans tmpdir; isolate it and provide a test input.
mkdir test-private-tmp
export TMPDIR="$PWD/test-private-tmp"
touch "$TMPDIR/seed"
%{__perl} -MTest::Pod -e 1
%make_build test

%files
%license lib/File/NCopy.pm
%doc Changes Contributing.txt
%{perl_vendorlib}/File/NCopy.pm
%{_mandir}/man3/File::NCopy.3*

%changelog
* Sun Nov 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.36-1
- Package official CPAN release with original tests.
