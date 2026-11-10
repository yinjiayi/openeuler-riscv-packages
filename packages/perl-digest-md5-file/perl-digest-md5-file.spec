# SPDX-License-Identifier: Apache-2.0
%global _default_patch_fuzz 0
Name:           perl-digest-md5-file
Version:        0.08
Release:        1%{?dist}
Summary:        Compute MD5 digests of local files, directories and URLs in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Digest-MD5-File
Source0:        https://cpan.metacpan.org/authors/id/D/DM/DMUEY/Digest-MD5-File-%{version}.tar.gz
Patch0:         0001-open-literal-filenames.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Encode)
BuildRequires:  patch
Requires:       perl(Carp)
Requires:       perl(Exporter)
Requires:       perl(Digest::MD5)
Requires:       perl(LWP::UserAgent)
Requires:       perl(File::Spec)
Requires:       perl(Encode)

%description
Compute MD5 digests of local files, directories and URLs in Perl

%prep
%setup -q -n Digest-MD5-File-%{version}
%patch -P 0 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install

%check
make test

%files
%license README
%doc Changes
%{perl_vendorlib}/Digest/MD5/File.pm
%{_mandir}/man3/Digest::MD5::File.3pm*

%changelog
* Sun Nov 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.08-1
- Package fixed release, retain original tests, and read literal local filenames.
