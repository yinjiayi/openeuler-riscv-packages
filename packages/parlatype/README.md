<!-- SPDX-License-Identifier: Apache-2.0 -->
# parlatype

This directory packages upstream `https://github.com/gkarsay/parlatype` version `4.0` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. Upstream `4.3` remains the latest detected stable release.

A **target-stack-compatible release** is the newest stable upstream release whose declared build interfaces can be provided at the required versions by the immutable target repository. Upstream `4.3` requires GTK `>= 4.14` and libadwaita `>= 1.5`; releases `4.1` and `4.2` require GTK `>= 4.10` and libadwaita `>= 1.4`. The fixed openEuler repository provides GTK `4.10.5`, GLib `2.78.3`, and libadwaita `1.3.4`, making `4.0` the newest compatible stable release because it requires GTK `>= 4.0`, GLib `>= 2.58`, and no libadwaita.

The official `v4.0` tag archive has SHA-256 `0f24df07a7d5afa30d306c7d56d145b7deba6eb9ce1952c2604599c638b4bc9c`. Its 626 members are contained in the single `parlatype-4.0` source root, with no absolute paths, parent traversal, links, or special files; the top-level `COPYING` and source headers confirm `GPL-3.0-or-later`.

Release `3` declares the direct providers used by the default Meson build and complete test suite: GTK and GLib development metadata, GStreamer core and base-plugin development metadata, the Good runtime plugins exercised by supported media, ISO Codes metadata/data, gettext, Yelp help tools, and the Meson/Ninja C toolchain. Optional GIR, gtk-doc, PocketSphinx, and DeepSpeech features retain their upstream-disabled defaults.

Exact-head Package CI run `33674786657` built and installed release `3`, then ran all eight upstream Meson tests. Five passed; the GTK `config` and `waveviewer` tests had no display, and the `player` test had no audio device. Release `4` adds openEuler's `xorg-x11-server-Xvfb` test provider and runs the same complete suite with a virtual X display and ALSA null device. No test is removed, skipped, or converted to an expected failure.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

Package CI run `33671468530` for exact head `e6fdf4134c1e0bed41c9166a14e9cb562ed782ee` first established the missing GTK provider. Run `33672605181` for exact head `9a69f7a101266d35dd8f62be1f2abfe56e1dc9d5` then completed dependency installation and proved the remaining `4.3` versus GTK `4.10.5` version incompatibility. Run `33674786657` for exact head `15e3070897fdb724bb1f27f9569e98b3f2ae6504` established the missing headless display and audio fixtures. Fresh target CI for release `4` remains authoritative.
