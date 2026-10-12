# SPDX-License-Identifier: Apache-2.0
Name:           perl-Text-Patch
Version:        1.8
Release:        1%{?dist}
Summary:        Apply unified, context, and old-style diffs to text
License:        GPL-2.0-only
URL:            https://metacpan.org/dist/Text-Patch
Source0:        Text-Patch-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Text-Diff
BuildRequires:  perl-generators
Requires:       perl(Text::Diff)

%description
Text::Patch applies unified, context, or old-style diff data to a string.

%prep
%autosetup -n Text-Patch-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
# Retain the original default upstream test unchanged; it has one placeholder
# assertion and explicitly disables substantive cases due to a newline issue.
# The installed-RPM smoke separately checks a real unified patch.
%make_build test

%files
%license COPYING
%doc README ChangeLog
%{perl_vendorlib}/Text/Patch.pm
%{_mandir}/man3/Text::Patch.3*

%changelog
* Sat Oct 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8-1
- Package official CPAN release with unchanged upstream check and functional smoke.
