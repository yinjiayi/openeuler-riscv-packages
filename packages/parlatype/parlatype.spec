# SPDX-License-Identifier: Apache-2.0
Name:           parlatype
Version:        4.0
Release:        7%{?dist}
Summary:        GNOME audio player for transcription
License:        GPL-3.0-or-later
URL:            https://github.com/gkarsay/parlatype
Source0:        parlatype-4.0.tar.gz
BuildRequires:  dbus-x11
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  gstreamer1-plugins-good
BuildRequires:  gtk4-devel
BuildRequires:  iso-codes-devel
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  yelp-tools
Requires:       gstreamer1-plugins-good
Requires:       iso-codes

%description
GNOME audio player for transcription

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
mkdir -p .test-runtime
chmod 0700 .test-runtime
printf 'pcm.!default { type null }\n' > alsa-null.conf
export ALSA_CONFIG_PATH="$PWD/alsa-null.conf"
export XDG_RUNTIME_DIR="$PWD/.test-runtime"
export GTK_A11Y=test
xvfb-run -a %{__meson} test \
  -C %{_vpath_builddir} \
  --num-processes %{_smp_build_ncpus} \
  --print-errorlogs

%files -f %{name}.files
%license COPYING
%doc README.md
%doc NEWS

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.0-7
- Use GTK's test accessibility backend for the headless test suite.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.0-6
- Add dbus-x11 so GTK tests can acquire their session bus under Xvfb.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.0-5
- Pass Meson's complete test command explicitly to the Xvfb wrapper.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.0-4
- Run the complete Meson suite with a virtual X display and ALSA null device.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.0-3
- Select the newest stable release compatible with the fixed target GTK stack.
- Declare the direct build, test, help, translation, and runtime providers.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.3-2
- Add the GTK 4 development dependency required by Meson.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.3-1
- Initial openEuler RISC-V package from the full package inventory.
