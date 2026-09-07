# SPDX-License-Identifier: Apache-2.0
Name:           gtk4-layer-shell
Version:        1.3.0
Release:        5%{?dist}
Summary:        Library to create panels and other desktop components for Wayland
License:        MIT
URL:            https://github.com/wmww/gtk4-layer-shell
Source0:        gtk4-layer-shell-1.3.0.tar.gz
Patch0:         0001-tests-allow-timeout-multiplier.patch
BuildRequires:  gcc
BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk4-devel
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  python3
BuildRequires:  python3-gobject
BuildRequires:  vala
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel

%description
Library to create panels and other desktop components for Wayland

%prep
%autosetup -p1

%build
%meson \
  -Dtests=true
%meson_build
# The upstream smoke tests execute these examples, but Meson deliberately
# excludes them from the default build when examples are not installed.
meson compile -C %{_vpath_builddir} \
  gtk4-layer-demo \
  simple-example-c \
  session-lock-c

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
export GTKLS_TEST_TIMEOUT_MULTIPLIER=10
meson test -C %{_vpath_builddir} \
  --num-processes %{_smp_build_ncpus} \
  --print-errorlogs \
  --timeout-multiplier "$GTKLS_TEST_TIMEOUT_MULTIPLIER"

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.0-5
- Scale Meson's outer per-test timeout together with the internal QEMU deadlines.

* Wed Sep 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.0-4
- Export the QEMU test-timeout multiplier so Meson test children inherit it.

* Wed Sep 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.0-3
- Scale the upstream integration-test deadlines under qemu-user without skipping tests.

* Wed Sep 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.0-2
- Declare the complete GTK4, Wayland, introspection, Vala, and Python test closure.
- Enable the full upstream test suite and build its smoke-only example targets.

* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
