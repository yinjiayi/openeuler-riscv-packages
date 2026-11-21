# SPDX-License-Identifier: Apache-2.0
Name:           perl-Pod-Spell-CommonMistakes
Version:        1.002
Release:        1%{?dist}
Summary:        Find common spelling and capitalization mistakes in POD
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Pod-Spell-CommonMistakes
Source0:        Pod-Spell-CommonMistakes-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-Module-Build-Tiny >= 0.039
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-IO-stringy
BuildRequires:  perl-Pod-Spell
BuildRequires:  perl-CPAN-Meta
BuildRequires:  perl-File-Temp
BuildRequires:  perl-PathTools
BuildRequires:  perl-Exporter
BuildRequires:  perl-parent
BuildRequires:  perl-generators
Requires:       perl(Pod::Spell) >= 1.01
Requires:       perl(IO::Scalar) >= 2.110

%description
Pod::Spell::CommonMistakes checks Perl POD documentation for common spelling
and capitalization mistakes using its included wordlists. It reports suggested
corrections without requiring a system spell checker.

%prep
%autosetup -n Pod-Spell-CommonMistakes-%{version} -p1

%build
%{__perl} Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=%{buildroot} --create_packlist=0

%check
# Keep all three upstream default test files and their original optional policy.
./Build test

%files
%license LICENSE
%doc README Changes AUTHOR_PLEDGE
%{perl_vendorlib}/Pod/Spell/CommonMistakes.pm
%{perl_vendorlib}/Pod/Spell/CommonMistakes/
%{_mandir}/man3/Pod::Spell::CommonMistakes.3*
%{_mandir}/man3/Pod::Spell::CommonMistakes::WordList.3*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.002-1
- Package the official CPAN release without changing its default tests.
