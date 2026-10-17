# SPDX-License-Identifier: MIT
Name:           libsoundio
Version:        2.0.0
Release:        1%{?dist}
Summary:        Cross-platform audio input and output library
License:        MIT
URL:            https://github.com/andrewrk/libsoundio
Source0:        libsoundio-2.0.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  cmake
BuildRequires:  glibc-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  binutils
BuildRequires:  rpm
BuildRequires:  gzip
BuildRequires:  tar
BuildRequires:  grep
BuildRequires:  gawk
BuildRequires:  sed
BuildRequires:  findutils
BuildRequires:  diffutils
Requires:       bash
Requires:       coreutils
Requires:       gcc
Requires:       glibc-devel
Requires:       alsa-lib-devel
Requires:       pulseaudio-libs-devel
Requires:       jack-audio-connection-kit-devel
Requires:       binutils
Requires:       grep

%description
C audio input/output library with Linux JACK, PulseAudio, ALSA and dummy
backends. Includes the default static/shared libraries, headers and examples,
all original test executables, and a separate installed public-API contract.
No audible, hardware, hotplug, native timing or performance validation is
claimed by the headless dummy-backend checks.

%prep
%setup -q -n libsoundio-dc4f84339039ac518b6cd1c0e7683e88e25be470
mkdir downstream
cat > downstream/consumer.c <<'C'
#undef NDEBUG
#include <soundio/soundio.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>

static void write_callback(struct SoundIoOutStream *stream, int minimum, int maximum) {
    (void)stream; (void)minimum; (void)maximum;
}

int main(void) {
    assert(strcmp(soundio_version_string(), "2.0.0") == 0);
    assert(soundio_version_major() == 2);
    assert(soundio_version_minor() == 0);
    assert(soundio_version_patch() == 0);
    assert(soundio_have_backend(SoundIoBackendJack));
    assert(soundio_have_backend(SoundIoBackendPulseAudio));
    assert(soundio_have_backend(SoundIoBackendAlsa));
    assert(soundio_have_backend(SoundIoBackendDummy));
    struct SoundIo *s = soundio_create();
    assert(s);
    assert(soundio_backend_count(s) >= 4);
    assert(soundio_connect_backend(s, SoundIoBackendDummy) == 0);
    assert(s->current_backend == SoundIoBackendDummy);
    soundio_flush_events(s);
    assert(soundio_input_device_count(s) == 1);
    assert(soundio_output_device_count(s) == 1);
    int index = soundio_default_output_device_index(s);
    assert(index >= 0);
    struct SoundIoDevice *device = soundio_get_output_device(s, index);
    assert(device && !device->probe_error);
    assert(soundio_device_supports_format(device, SoundIoFormatFloat32NE));
    assert(soundio_device_supports_sample_rate(device, 48000));
    struct SoundIoOutStream *stream = soundio_outstream_create(device);
    assert(stream);
    stream->format = SoundIoFormatFloat32NE;
    stream->sample_rate = 48000;
    stream->layout = device->layouts[0];
    stream->write_callback = write_callback;
    assert(soundio_outstream_open(stream) == 0);
    soundio_outstream_destroy(stream);
    soundio_device_unref(device);
    struct SoundIoRingBuffer *ring = soundio_ring_buffer_create(s, 32);
    assert(ring && soundio_ring_buffer_capacity(ring) >= 32);
    const char payload[] = "installed-libsoundio";
    memcpy(soundio_ring_buffer_write_ptr(ring), payload, sizeof(payload));
    soundio_ring_buffer_advance_write_ptr(ring, (int)sizeof(payload));
    assert(soundio_ring_buffer_fill_count(ring) == (int)sizeof(payload));
    assert(memcmp(soundio_ring_buffer_read_ptr(ring), payload, sizeof(payload)) == 0);
    soundio_ring_buffer_advance_read_ptr(ring, (int)sizeof(payload));
    assert(soundio_ring_buffer_fill_count(ring) == 0);
    soundio_ring_buffer_destroy(ring);
    soundio_disconnect(s);
    soundio_destroy(s);
    puts("public API: version, all Linux backends compiled, dummy devices/stream, ring buffer OK");
    return 0;
}
C
cat > downstream/run-contract.sh <<'SH'
#!/usr/bin/env bash
set -euxo pipefail
root=${1:?staged or installed root required}
prefix="${root%/}/usr"
testroot="$prefix/share/libsoundio/tests"
work=$(mktemp -d)
trap 'rm -r -- "$work"' EXIT
export LD_LIBRARY_PATH="$prefix/lib64"
export GCOV_PREFIX="$work/gcov"
export GCOV_PREFIX_STRIP=0
cd "$testroot"
sha256sum -c upstream.sha256
sha256sum -c binaries.sha256
test -f "$prefix/lib64/libsoundio.a"
test -L "$prefix/lib64/libsoundio.so"
test -L "$prefix/lib64/libsoundio.so.2"
readelf -d "$prefix/lib64/libsoundio.so.2.0.0" > "$work/elf.txt"
grep -F 'Library soname: [libsoundio.so.2]' "$work/elf.txt"
for original in unit_tests latency underflow backend_disconnect_recover overflow; do
    test -x "$prefix/libexec/libsoundio/$original"
done
for original in sio_sine sio_list_devices sio_microphone sio_record; do
    test -x "$prefix/bin/$original"
done
# The unchanged upstream executable embeds private source objects. It is not
# an installed shared-library conformance test; the two public consumers below are.
if timeout 600 "$prefix/libexec/libsoundio/unit_tests" > "$work/unit.log" 2>&1; then
    :
else
    status=$?
    cat "$work/unit.log"
    exit "$status"
fi
cat "$work/unit.log"
test "$(grep -c '^testing ' "$work/unit.log")" -eq 6
test "$(grep -c 'OK$' "$work/unit.log")" -eq 6
for original in 'os_get_time' 'create output stream' 'mirrored memory' 'soundio_device_nearest_sample_rate' 'ring buffer basic' 'ring buffer threaded'; do
    grep -F "testing $original..." "$work/unit.log"
done
if timeout 60 "$prefix/bin/sio_list_devices" --backend dummy --short > "$work/devices.log" 2>&1; then
    :
else
    status=$?
    cat "$work/devices.log"
    exit "$status"
fi
cat "$work/devices.log"
grep -F '2 devices found' "$work/devices.log"
cc -std=c11 -O2 -g -UNDEBUG -Wall -Wextra -Werror -I"$prefix/include" \
    "$testroot/consumer.c" -L"$prefix/lib64" -Wl,-rpath,"$prefix/lib64" \
    -lsoundio -o "$work/shared-consumer"
timeout 60 "$work/shared-consumer"
cc -std=c11 -O2 -g -UNDEBUG -Wall -Wextra -Werror -I"$prefix/include" \
    "$testroot/consumer.c" "$prefix/lib64/libsoundio.a" \
    -ljack -lpulse -lasound -lpthread -lm -o "$work/static-consumer"
timeout 60 "$work/static-consumer"
SH

%build
export CFLAGS="%{optflags} -g -UNDEBUG"
# Preserve upstream Debug and all default ON targets/backends; never filter tests.
cmake -S . -B build -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DCMAKE_INSTALL_INCLUDEDIR=include -DCMAKE_INSTALL_BINDIR=bin
for backend in JACK PULSEAUDIO ALSA; do
    grep -E "^#define SOUNDIO_HAVE_${backend}([[:space:]]|$)" build/config.h
done
make -C build %{?_smp_mflags}

%install
DESTDIR=%{buildroot} cmake --install build
install -d %{buildroot}%{_libexecdir}/libsoundio %{buildroot}%{_datadir}/libsoundio/tests/upstream
for original in unit_tests latency underflow backend_disconnect_recover overflow; do
    install -m 0755 build/$original %{buildroot}%{_libexecdir}/libsoundio/$original
done
install -m 0644 downstream/consumer.c downstream/run-contract.sh %{buildroot}%{_datadir}/libsoundio/tests/
cp -p CMakeLists.txt LICENSE README.md test/unit_tests.c %{buildroot}%{_datadir}/libsoundio/tests/upstream/
(cd %{buildroot}%{_datadir}/libsoundio/tests && sha256sum upstream/* > upstream.sha256)
%check
# Bind final post-BRP/strip bytes, not earlier unstripped install outputs.
(cd %{buildroot}%{_datadir}/libsoundio/tests && \
    sha256sum ../../../libexec/libsoundio/* ../../../bin/sio_* ../../../lib64/libsoundio.so.2.0.0 ../../../lib64/libsoundio.a > binaries.sha256)
# Full no-argument original unit suite plus staged installed-public-API checks.
bash %{buildroot}%{_datadir}/libsoundio/tests/run-contract.sh %{buildroot}

%files
%license LICENSE
%doc README.md
%{_libdir}/libsoundio.so*
%{_libdir}/libsoundio.a
%{_includedir}/soundio/
%{_bindir}/sio_sine
%{_bindir}/sio_list_devices
%{_bindir}/sio_microphone
%{_bindir}/sio_record
%{_libexecdir}/libsoundio/
%{_datadir}/libsoundio/

%changelog
* Fri Oct 16 2026 Codex <noreply@openai.com> - 2.0.0-1
- Package fixed official source with original defaults and six unfiltered tests
- Separate installed shared/static API checks from native hardware/timing claims
