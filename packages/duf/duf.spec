# SPDX-License-Identifier: Apache-2.0
Name:           duf
Version:        0.9.1
Release:        1%{?dist}
%global debug_package %{nil}
Summary:        Disk Usage/Free Utility
License:        MIT
URL:            https://github.com/muesli/duf
Source0:        duf-0.9.1.tar.gz

BuildRequires:  golang


%description
duf is a terminal utility that reports disk usage and free space for local,
network, FUSE, and other mounted filesystems.

%prep
%autosetup -p1

%build
%set_build_flags
go build -buildvcs=false -trimpath \
  -ldflags "-s -w -X main.Version=%{version}" \
  -o duf .

%install
install -Dpm0755 duf %{buildroot}%{_bindir}/duf
install -Dpm0644 duf.1 %{buildroot}%{_mandir}/man1/duf.1

%check
go test -count=1 ./...
./duf --version | grep -F "duf %{version}"

%files
%license LICENSE
%doc README.md
%{_bindir}/duf
%{_mandir}/man1/duf.1*

%changelog
* Fri Aug 21 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.1-1
- Package the upstream stable release with its Go unit tests and manual page.
