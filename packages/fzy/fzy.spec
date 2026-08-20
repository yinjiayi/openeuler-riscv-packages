# SPDX-License-Identifier: Apache-2.0

Name:           fzy
Version:        1.1
Release:        1%{?dist}
Summary:        Fast terminal fuzzy text selector
License:        MIT AND ISC
URL:            https://github.com/jhawthorn/fzy
Source0:        fzy-%{version}.tar.gz
Source1:        ttytest-0.6.0.gem

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ruby
BuildRequires:  rubygem-minitest
BuildRequires:  rubygems
BuildRequires:  tmux

%description
fzy is a fast terminal fuzzy selector that ranks matching input lines while
favoring consecutive characters, word starts, compact matches, and short
candidates.

%prep
%autosetup -p1
gem unpack %{SOURCE1} --target .test-vendor

%build
%make_build \
  CFLAGS="%{optflags} -MD -Wall -Wextra -std=c99 -pedantic -Ideps -Werror=vla" \
  CCFLAGS="%{build_ldflags}"

%install
%make_install \
  PREFIX=%{_prefix} \
  MANDIR=%{_mandir} \
  CFLAGS="%{optflags} -MD -Wall -Wextra -std=c99 -pedantic -Ideps -Werror=vla" \
  CCFLAGS="%{build_ldflags}"

%check
%make_build check \
  CFLAGS="%{optflags} -MD -Wall -Wextra -std=c99 -pedantic -Ideps -Werror=vla" \
  CCFLAGS="%{build_ldflags}"
LC_ALL=C.UTF-8 TERM=xterm-256color \
  ruby -I.test-vendor/ttytest-0.6.0/lib test/acceptance/acceptance_test.rb

%files
%license LICENSE
%doc ALGORITHM.md CHANGELOG.md README.md
%{_bindir}/fzy
%{_mandir}/man1/fzy.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1-1
- Initial openEuler RISC-V package with all unit/property and TTY acceptance tests.
