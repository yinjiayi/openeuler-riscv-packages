<!-- SPDX-License-Identifier: Apache-2.0 -->
# SDL2_mixer

SDL2_mixer 2.8.2 for openEuler 24.03 LTS SP3 on riscv64/RVA23. The
official current SDL 2-series release asset is pinned by SHA-256 and its archive
was safety-inspected before onboarding. Frozen Ubuntu 26.04 source metadata at
2.8.1 is the inventory lineage; no external package recipe was executed.

The fixed openEuler repository provides SDL2-devel and each selected external
codec development dependency. The build links libFLAC, FluidSynth, ModPlug,
libvorbis, mpg123, opusfile, and WavPack directly instead of silently loading
optional libraries. Upstream Timidity MIDI support stays enabled. The build
runs upstream's complete release-version consistency test; the installed smoke
test initializes every advertised format decoder with SDL's dummy audio driver,
loads an in-memory PCM WAVE sample, and starts playback without audio hardware.

Apache-2.0 covers the packaging files; upstream source remains Zlib-licensed.
