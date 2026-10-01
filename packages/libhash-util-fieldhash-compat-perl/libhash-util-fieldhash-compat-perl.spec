# SPDX-License-Identifier: Apache-2.0
Name:           perl-Hash-Util-FieldHash-Compat
Version:        0.11
Release:        3%{?dist}
Summary:        Compatibility facade for Perl field hashes
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Hash-Util-FieldHash-Compat
Source0:        Hash-Util-FieldHash-Compat-%{version}.tar.gz

BuildArch:      noarch
# Compat.pm loads Heavy.pm only if native Hash::Util::FieldHash is unavailable.
# This fixed target hard-requires the native provider; RPM's static scanner
# otherwise adds an unresolvable dependency from the unreachable fallback.
# Keep Heavy.pm and its tests intact, excluding only that false-positive name.
%global __requires_exclude ^perl[(]Tie::RefHash::Weak[)]([[:space:]]|$)
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-PathTools
BuildRequires:  perl-Test-Simple
BuildRequires:  perl(Hash::Util::FieldHash)
BuildRequires:  perl-generators
Requires:       perl(Hash::Util::FieldHash)

%description
Hash::Util::FieldHash::Compat exposes Perl field-hash operations through a
compatibility API. On this target it delegates to Perl's native field hashes.

%prep
%autosetup -n Hash-Util-FieldHash-Compat-%{version} -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name perllocal.pod -delete

%check
%make_build test

%files
%license LICENCE
%doc README Changes
%{perl_vendorlib}/Hash/Util/FieldHash/Compat.pm
%{perl_vendorlib}/Hash/Util/FieldHash/Compat/Heavy.pm
%{_mandir}/man3/Hash::Util::FieldHash::Compat*.3*

%changelog
* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.11-3
- Match the generated versioned fallback dependency string in the narrow filter.

* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.11-2
- Exclude an unreachable older-Perl fallback auto-Requires on the fixed target.

* Thu Oct 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.11-1
- Package the official CPAN release with all default upstream tests.
