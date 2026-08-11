# SPDX-License-Identifier: Apache-2.0
Name:           checksec
Version:        3.2.0
Release:        1%{?dist}
Summary:        Inspect ELF binaries for hardening features
License:        BSD-3-Clause
URL:            https://github.com/slimm609/checksec.sh
Source0:        3.2.0.tar.gz

BuildArch:      noarch

BuildRequires:  binutils
BuildRequires:  file
BuildRequires:  findutils
BuildRequires:  gawk
BuildRequires:  jq
BuildRequires:  openssl
BuildRequires:  procps-ng
BuildRequires:  which
Requires:       bash
Requires:       binutils
Requires:       coreutils
Requires:       file
Requires:       findutils
Requires:       gawk
Requires:       grep
Requires:       jq
Requires:       openssl
Requires:       procps-ng
Requires:       sed
Requires:       which

%description
checksec inspects ELF binaries, processes, and kernel configuration for common
hardening features. This package follows the Fedora 44 GA 2.7.1 shell-script
baseline so the fixed openEuler target can build it entirely offline.

%prep
%autosetup -p1
# Use the deterministic system shell and disable the upstream self-update path.
sed -i '1s|^#!/usr/bin/env bash$|#!/usr/bin/bash|' checksec
sed -i 's/^pkg_release=false$/pkg_release=true/' checksec
grep -Fx '#!/usr/bin/bash' checksec
grep -Fx 'pkg_release=true' checksec

%build
bash -n checksec

%install
install -Dpm0755 checksec %{buildroot}%{_bindir}/checksec
install -Dpm0644 extras/man/checksec.1 %{buildroot}%{_mandir}/man1/checksec.1

%check
./checksec --version | grep -F 'checksec v%{version}'
if ./checksec --help | grep -E -- '--(update|upgrade)'; then
  echo 'packaged checksec unexpectedly exposes its network self-update command' >&2
  exit 1
fi
./checksec --format=json --file=/usr/bin/bash | jq -e 'type == "object"'

%files
%license LICENSE.txt
%doc ChangeLog README.md
%{_bindir}/checksec
%{_mandir}/man1/checksec.1*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.7.1-1
- Initial Fedora 44 baseline package with offline file-mode validation.
