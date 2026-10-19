# SPDX-License-Identifier: Apache-2.0
Name:           hyx
Version:        2026.01.11
Release:        1
Summary:        Minimalistic terminal hex editor
License:        MIT
URL:            https://yx7.cc/code
Source0:        hyx-2026.01.11.tar.xz
Source1:        tests/smoke.sh
Source2:        tests/pty-check.py
Patch0:         patches/0001-bound-terminal-input-and-empty-file-info.patch
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  xz
BuildRequires:  coreutils
BuildRequires:  patch
BuildRequires:  python3


%description
Hyx is a terminal hex editor with insert, replace, delete, copy/paste,
undo/redo, search and hexadecimal/ASCII input. It uses libc and POSIX
terminal interfaces without an external terminal-widget dependency.

%package tests
Summary:        Offline CLI and pseudoterminal checks for Hyx
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python3
Requires:       bash

%description tests
Bounded offline CLI and pseudoterminal regressions for the packaged editor.
These checks do not establish native terminal, signal or timing correctness.

%prep
%autosetup -n hyx-%{version} -p1

%build
# Keep the default target and all editor modes; retain assertions.
%make_build CC=gcc CFLAGS="%{optflags} -Wall -Wextra -std=c99 -pedantic" LDFLAGS="%{?build_ldflags}"

%install
install -Dpm0755 hyx %{buildroot}%{_bindir}/hyx
install -Dpm0755 %{SOURCE1} %{buildroot}%{_libexecdir}/hyx-tests/smoke.sh
install -Dpm0644 %{SOURCE2} %{buildroot}%{_libexecdir}/hyx-tests/pty-check.py

%check
# Upstream has no check/test target; default hyx build remains unchanged.
# Run the staged checks here and the same checks after normal installation.
python3 %{buildroot}%{_libexecdir}/hyx-tests/pty-check.py %{buildroot}

%files
%license license.txt
%{_bindir}/hyx

%files tests
%license license.txt
%{_libexecdir}/hyx-tests/

%changelog
* Mon Oct 19 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2026.01.11-1
- Onboard fixed official release with bounded terminal-input regressions.
