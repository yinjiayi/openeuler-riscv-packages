# SPDX-License-Identifier: Apache-2.0
Name:           perl-file-tempdir
Version:        0.02
Release:        1%{?dist}
Summary:        Object interface for managed temporary directories in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/File-Tempdir
Source0:        https://cpan.metacpan.org/authors/id/N/NA/NANARDON/File-Tempdir-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(Test::More)
Requires:       perl
Requires:       perl(File::Temp)
Requires:       perl(File::Path)

%description
Wrap File::Temp temporary directories in a Perl object that cleans up
directories it creates while retaining user-supplied directories.

%prep
%setup -q -n File-Tempdir-%{version}
sed -n '/^=head1 AUTHOR$/,$p' lib/File/Tempdir.pm > LICENSE-POD
test -s LICENSE-POD

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR="%{buildroot}"

%check
mkdir -p .rpm-test-tmp
TMPDIR="$PWD/.rpm-test-tmp" make test

%files
%license LICENSE-POD
%{perl_vendorlib}/File/Tempdir.pm
%{_mandir}/man3/File::Tempdir.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.02-1
- Package the official stable release and retain the original default tests.
