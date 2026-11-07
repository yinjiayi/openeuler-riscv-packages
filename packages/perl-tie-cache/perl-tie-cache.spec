# SPDX-License-Identifier: Apache-2.0
Name:           perl-Tie-Cache
Version:        0.21
Release:        1%{?dist}
Summary:        Perl least recently used cache with a tied hash interface
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/dist/Tie-Cache
Source0:        Tie-Cache-0.21.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-generators
Requires:       perl

%description
Tie::Cache implements a least recently used in-memory cache through a tied
Perl hash, with entry-count and approximate-size limits.

%prep
%autosetup -n Tie-Cache-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%make_build

%install
%make_install
find %{buildroot} -type f \( -name .packlist -o -name perllocal.pod \) -delete
# MakeMaker treats the optional comparison benchmark as an installable module.
# Keep it as documentation, not a vendorlib program with extra dependencies.
rm -f %{buildroot}%{perl_vendorlib}/Tie/tie-cache-bench.pl

%check
# Preserve the complete original default test command and propagate its status.
status=0
%make_build test > upstream-test.log 2>&1 || status=$?
cat upstream-test.log
if [ "$status" -ne 0 ]; then exit "$status"; fi
# Upstream prints ERROR without exiting nonzero. Require all eleven checks.
%{__perl} -e 'local $/; my $log = <>; die "upstream functional failure\n" if $log =~ /^ERROR\b/m; my @ok = $log =~ /^OK \.\.\. .+$/mg; die "expected 11 upstream functional checks\n" unless @ok == 11;' upstream-test.log

%files
%license Cache.pm
%doc README CHANGES
%attr(0644,root,root) %doc tie-cache-bench.pl
%{perl_vendorlib}/Tie/Cache.pm
%{_mandir}/man3/Tie::Cache.3*

%changelog
* Sat Nov 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.21-1
- Package the pinned release and preserve all original default tests.
- Fail closed on upstream functional errors and incomplete check output.
