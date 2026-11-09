# SPDX-License-Identifier: Apache-2.0
Name:           perl-text-quoted
Version:        2.10
Release:        1%{?dist}
Summary:        Extract the structure of quoted mail messages
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Text-Quoted
Source0:        Text-Quoted-%{version}.tar.gz
Source1:        LICENSE.ReadmeFromPod
Patch0:         0001-retain-vendored-installer-notices.patch
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.59
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-generators
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Text::Autoformat)
BuildRequires:  perl(Text::Tabs)
Requires:       perl
Requires:       perl(Text::Autoformat)
Requires:       perl(Text::Tabs)

%description
Extract the structure of quoted mail messages, including nested quote levels,
and combine the resulting hunks back into text.

%prep
%setup -q -n Text-Quoted-%{version}
%global _default_patch_fuzz 0
%patch -P 0 -p1
cp -p %{SOURCE1} LICENSE.ReadmeFromPod

%build
%{__perl} -I. Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}

%check
make test

%files
%license README NOTICE.Module-Install LICENSE.ReadmeFromPod
%doc Changes
%{perl_vendorlib}/Text/Quoted.pm
%{_mandir}/man3/Text::Quoted.3pm*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.10-1
- Package the pinned release, original tests and exact vendored-tool notices.
