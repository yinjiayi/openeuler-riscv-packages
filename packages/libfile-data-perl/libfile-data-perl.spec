# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-Data
Version:        1.20
Release:        1%{?dist}
Summary:        Read and write file data with a Perl object interface
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-Data
Source0:        File-Data-%{version}.tar.gz
Patch0:         0001-install-module-to-vendorlib-root.patch

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
# Perl compares Carp 1.50 above 1.3301; RPM version ordering does not.
BuildRequires:  perl-Carp >= 1.50
BuildRequires:  perl(Data::Dumper) >= 2.151
BuildRequires:  perl(Fcntl) >= 1.11
BuildRequires:  perl(FileHandle) >= 2.02
Requires:       perl-Carp >= 1.50

%description
File::Data provides an object interface for reading, writing and transforming
files, with file locking and explicit access modes.

%prep
%autosetup -n File-Data-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Keep the original t/test.t (16 assertions). It uses the source tree; also
# prove that the patched staged install can load the packaged module.
%{__perl} -MCarp -e 'Carp->VERSION(1.3301)'
%make_build test
test -f %{buildroot}%{perl_vendorlib}/File/Data.pm
PERL5LIB=%{buildroot}%{perl_vendorlib} %{__perl} -MFile::Data -e 'die "unexpected version\n" unless $File::Data::VERSION eq "1.20"'

%files
%license lib/File/Data.pm
%doc README Changes TODO
%{perl_vendorlib}/File/Data.pm
%{_mandir}/man3/File::Data.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.20-1
- Package official CPAN release and fix its installed Perl library path.
