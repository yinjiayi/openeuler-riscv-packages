# SPDX-License-Identifier: Apache-2.0

%global debug_package %{nil}

Name:           age
Version:        1.3.1
Release:        1%{?dist}
Summary:        A simple, modern and secure file encryption tool
License:        BSD-3-Clause
URL:            https://github.com/FiloSottile/age
Source0:        age-1.3.1.tar.gz
BuildRequires:  golang

%description
age is a simple, modern, and secure file encryption tool. It supports native
X25519 and passphrase recipients, SSH identities, and age plugins.

%prep
%autosetup -p1 -n age-%{version}

%build
export CGO_ENABLED=0
mkdir -p bin
for command in age age-keygen age-inspect age-plugin-batchpass; do
  go build -buildvcs=false -trimpath -ldflags "-X main.Version=v%{version}" \
    -o "bin/${command}" "./cmd/${command}"
done

%install
for command in age age-keygen age-inspect age-plugin-batchpass; do
  install -Dpm 0755 "bin/${command}" "%{buildroot}%{_bindir}/${command}"
done
for manual in age age-keygen age-inspect age-plugin-batchpass; do
  install -Dpm 0644 "doc/${manual}.1" \
    "%{buildroot}%{_mandir}/man1/${manual}.1"
done

%check
export GOFLAGS=-buildvcs=false
go test -timeout 30m ./...
for command in age age-keygen age-inspect age-plugin-batchpass; do
  "bin/${command}" --version | grep -Fx 'v%{version}'
done

%files
%license LICENSE
%doc README.md SIGSUM.md
%{_bindir}/age
%{_bindir}/age-keygen
%{_bindir}/age-inspect
%{_bindir}/age-plugin-batchpass
%{_mandir}/man1/age.1*
%{_mandir}/man1/age-keygen.1*
%{_mandir}/man1/age-inspect.1*
%{_mandir}/man1/age-plugin-batchpass.1*

%changelog
* Fri Aug 21 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.1-1
- Initial openEuler RISC-V package with the upstream Go test suite.
