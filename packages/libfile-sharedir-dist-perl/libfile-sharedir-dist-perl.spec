# SPDX-License-Identifier: Apache-2.0
Name:           perl-File-ShareDir-Dist
Version:        0.07
Release:        1%{?dist}
Summary:        Locate per-distribution shared files in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/File-ShareDir-Dist
Source0:        File-ShareDir-Dist-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
BuildRequires:  perl(File::Copy)

%description
File::ShareDir::Dist locates shared data for Perl distributions. The
distribution also includes an installer and test-harness plugins.

%prep
%autosetup -n File-ShareDir-Dist-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Preserve all six upstream default test files and their corpus fixtures.
%make_build test
test -f %{buildroot}%{perl_vendorlib}/File/ShareDir/Dist.pm
PERL5LIB=%{buildroot}%{perl_vendorlib} %{__perl} -MFile::ShareDir::Dist -e 'die "unexpected version\n" unless $File::ShareDir::Dist::VERSION eq "0.07"'

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/File/ShareDir/Dist.pm
%{perl_vendorlib}/File/ShareDir/Dist/Install.pm
%{perl_vendorlib}/App/Prove/Plugin/ShareDirDist.pm
%{perl_vendorlib}/App/Yath/Plugin/ShareDirDist.pm
%{_mandir}/man3/File::ShareDir::Dist.3*
%{_mandir}/man3/File::ShareDir::Dist::Install.3*
%{_mandir}/man3/App::Prove::Plugin::ShareDirDist.3*
%{_mandir}/man3/App::Yath::Plugin::ShareDirDist.3*

%changelog
* Fri Oct 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.07-1
- Package official CPAN release with unchanged upstream default tests.
