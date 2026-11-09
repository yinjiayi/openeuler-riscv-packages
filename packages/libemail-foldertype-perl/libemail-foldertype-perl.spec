# SPDX-License-Identifier: Apache-2.0
Name:           libemail-foldertype-perl
Version:        0.814
Release:        1%{?dist}
Summary:        Recognize mail folder types in Perl
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Email-FolderType
Source0:        Email-FolderType-0.814.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(Module::Pluggable)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  perl(Capture::Tiny)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(blib)
Requires:       perl
Requires:       perl(Exporter) >= 5.57
Requires:       perl(Module::Pluggable)
Requires:       perl(strict)
Requires:       perl(warnings)

%description
Recognize mail folder types in Perl

%prep
%autosetup -n Email-FolderType-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install DESTDIR=%{buildroot}
test -f %{buildroot}%{perl_vendorlib}/Email/FolderType.pm
test -f %{buildroot}%{_mandir}/man3/Email::FolderType.3pm
for matcher in Ezmlm MH Maildir Mbox; do
    test -f "%{buildroot}%{perl_vendorlib}/Email/FolderType/${matcher}.pm"
    test -f "%{buildroot}%{_mandir}/man3/Email::FolderType::${matcher}.3pm"
done

%check
make test TEST_VERBOSE=1

%files
%license LICENSE
%doc README Changes
%{perl_vendorlib}/Email/FolderType.pm
%dir %{perl_vendorlib}/Email/FolderType
%{perl_vendorlib}/Email/FolderType/Ezmlm.pm
%{perl_vendorlib}/Email/FolderType/MH.pm
%{perl_vendorlib}/Email/FolderType/Maildir.pm
%{perl_vendorlib}/Email/FolderType/Mbox.pm
%{_mandir}/man3/Email::FolderType.3pm*
%{_mandir}/man3/Email::FolderType::Ezmlm.3pm*
%{_mandir}/man3/Email::FolderType::MH.3pm*
%{_mandir}/man3/Email::FolderType::Maildir.3pm*
%{_mandir}/man3/Email::FolderType::Mbox.3pm*

%changelog
* Mon Nov 09 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.814-1
- Package verified source, original tests and all five installed modules.
