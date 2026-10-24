# SPDX-License-Identifier: Apache-2.0
Name:           libsmf
Version:        1.3
Release:        1%{?dist}
Summary:        Standard MIDI File handling library and shell
License:        BSD-2-Clause AND GPL-3.0-or-later AND (GPL-2.0-or-later WITH Autoconf-exception-generic) AND (GPL-2.0-or-later WITH Libtool-exception) AND FSFAP AND FSFUL AND X11 AND ISC
URL:            https://sourceforge.net/projects/libsmf/
Source0:        libsmf-1.3.tar.gz
Source1:        gpl-2.0.txt
Source2:        gpl-3.0.txt
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  glib2-devel
BuildRequires:  grep
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  readline-devel
BuildRequires:  sed
Requires:       bash
Requires:       coreutils
Requires:       grep

%description
Read and write Standard MIDI Files, including tracks, event ordering and
arithmetic tempo maps. Keep the default shared/static libraries and the
Readline-linked interactive smfsh, with deterministic API regressions.

%prep
%autosetup -n libsmf-1.3 -p1
# Preserve all 36 original source members before configure's normal active
# helper refresh. Inert suffixes prevent recursive macro replacement of notices.
find . -path ./license-notices -prune -o -type f -print | while IFS= read -r original; do
    mkdir -p "license-notices/$(dirname "$original")"
    cp -p "$original" "license-notices/$original.notice"
done
cp -p %{SOURCE1} license-notices/GPL-2.0.txt
cp -p %{SOURCE2} license-notices/GPL-3.0.txt
(cd license-notices; find . -type f -print | LC_ALL=C sort | xargs sha256sum) > original-notices.sha256
mv original-notices.sha256 license-notices/SHA256SUMS
find license-notices -type f -exec chmod 0644 {} +
test "$(find license-notices -type f | wc -l)" -eq 39
cat > api-smoke.c <<'LIBSMF_API_EOF'
/*
 * Copyright 2026 openEuler RISC-V package contributors.
 * SPDX-License-Identifier: ISC
 * Permission to use, copy, modify, and/or distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION
 * OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
 * CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */
#include <smf.h>
#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static smf_event_t *note(int status, int pitch, int velocity) {
    smf_event_t *event = smf_event_new_from_bytes(status, pitch, velocity);
    assert(event != NULL && smf_event_is_valid(event));
    return event;
}
static smf_track_t *track(smf_t *song) {
    smf_track_t *t = smf_track_new();
    assert(t != NULL);
    smf_add_track(song, t);
    return t;
}
static void close_to(double actual, double expected) {
    assert(fabs(actual - expected) < 1e-9);
}
static void path(char *out, size_t length, const char *directory, const char *name) {
    int n = snprintf(out, length, "%s/%s", directory, name);
    assert(n > 0 && (size_t)n < length);
}
static unsigned char *read_file(const char *name, size_t *length) {
    FILE *f = fopen(name, "rb");
    assert(f != NULL && fseek(f, 0, SEEK_END) == 0);
    long size = ftell(f);
    assert(size > 0 && size < 4096 && fseek(f, 0, SEEK_SET) == 0);
    unsigned char *bytes = malloc((size_t)size);
    assert(bytes != NULL && fread(bytes, 1, (size_t)size, f) == (size_t)size);
    assert(fclose(f) == 0);
    *length = (size_t)size;
    return bytes;
}
static void decoded(smf_t *song) {
    assert(song != NULL && song->format == 0 && song->ppqn == 480);
    assert(song->number_of_tracks == 1);
    smf_track_t *t = smf_get_track_by_number(song, 1);
    assert(t != NULL && t->number_of_events == 4);
    smf_event_t *on = smf_track_get_event_by_number(t, 2);
    smf_event_t *off = smf_track_get_event_by_number(t, 3);
    const unsigned char expected_on[] = {0x90, 60, 100};
    const unsigned char expected_off[] = {0x80, 60, 0};
    assert(on != NULL && off != NULL);
    assert(on->midi_buffer_length == 3 && off->midi_buffer_length == 3);
    assert(memcmp(on->midi_buffer, expected_on, 3) == 0);
    assert(memcmp(off->midi_buffer, expected_off, 3) == 0);
    assert(on->time_pulses == 0 && off->time_pulses == 480);
    close_to(off->time_seconds, 0.5);
    assert(smf_event_is_eot(smf_track_get_event_by_number(t, 4)));
}
int main(int argc, char **argv) {
    assert(argc == 2);
    setvbuf(stdout, NULL, _IONBF, 0);
    char file[4096];
    path(file, sizeof(file), argv[1], "single.mid");
    smf_t *song = smf_new();
    assert(song != NULL && strcmp(smf_get_version(), "1.3") == 0);
    assert(song->format == 0 && song->ppqn == 120 && song->number_of_tracks == 0);
    smf_tempo_t *tempo = smf_get_tempo_by_number(song, 0);
    assert(tempo != NULL && tempo->microseconds_per_quarter_note == 500000);
    assert(smf_set_ppqn(song, 480) == 0);
    puts("API case1 version-defaults PASS");

    smf_track_t *t = track(song);
    unsigned char initial_tempo[] = {0xff, 0x51, 3, 7, 0xa1, 0x20};
    smf_event_t *event = smf_event_new_from_pointer(initial_tempo, sizeof(initial_tempo));
    assert(event != NULL && smf_event_is_valid(event));
    smf_track_add_event_pulses(t, event, 0);
    smf_track_add_event_pulses(t, note(0x90, 60, 100), 0);
    smf_track_add_event_pulses(t, note(0x80, 60, 0), 480);
    assert(smf_save(song, file) == 0);
    const unsigned char expected_wire[] = {
        'M','T','h','d',0,0,0,6,0,0,0,1,1,0xe0,
        'M','T','r','k',0,0,0,20,
        0,0xff,0x51,3,7,0xa1,0x20,
        0,0x90,60,100,0x83,0x60,0x80,60,0,0,0xff,0x2f,0
    };
    size_t length = 0;
    unsigned char *bytes = read_file(file, &length);
    assert(length == sizeof(expected_wire) && memcmp(bytes, expected_wire, length) == 0);
    smf_delete(song);
    puts("API case2 exact-wire-encoding PASS");

    song = smf_load_from_memory(bytes, (int)length);
    decoded(song);
    smf_rewind(song);
    int count = 0;
    while ((event = smf_get_next_event(song)) != NULL) { assert(smf_event_is_valid(event)); ++count; }
    assert(count == 4);
    smf_delete(song); free(bytes);
    song = smf_load(file); decoded(song);
    assert(smf_seek_to_pulses(song, 480) == 0);
    event = smf_get_next_event(song);
    assert(event != NULL && event->midi_buffer[0] == 0x80 && event->time_pulses == 480);
    smf_delete(song);
    puts("API case3 memory-file-decode-and-seek PASS");

    song = smf_new(); assert(song != NULL && smf_set_ppqn(song, 480) == 0);
    t = track(song);
    smf_track_add_event_pulses(t, note(0x90, 64, 90), 0);
    unsigned char faster[] = {0xff, 0x51, 3, 3, 0xd0, 0x90};
    event = smf_event_new_from_pointer(faster, sizeof(faster)); assert(event != NULL);
    smf_track_add_event_pulses(t, event, 480);
    event = note(0x80, 64, 0); smf_track_add_event_pulses(t, event, 960);
    close_to(event->time_seconds, 0.75);
    tempo = smf_get_tempo_by_pulses(song, 960);
    assert(tempo != NULL && tempo->time_pulses == 480 && tempo->microseconds_per_quarter_note == 250000);
    path(file, sizeof(file), argv[1], "tempo.mid"); assert(smf_save(song, file) == 0); smf_delete(song);
    song = smf_load(file); assert(song != NULL);
    event = smf_track_get_event_by_number(smf_get_track_by_number(song, 1), 3);
    assert(event != NULL && event->time_pulses == 960); close_to(event->time_seconds, 0.75);
    close_to(smf_get_length_seconds(song), 0.75); smf_delete(song);
    puts("API case4 tempo-map-arithmetic-roundtrip PASS");

    song = smf_new(); assert(song != NULL);
    smf_track_t *first = track(song), *second = track(song);
    assert(song->format == 1 && smf_set_format(song, 1) == 0);
    smf_track_add_event_pulses(first, note(0x90, 60, 80), 0);
    smf_track_add_event_pulses(second, note(0x91, 67, 70), 120);
    path(file, sizeof(file), argv[1], "multi.mid"); assert(smf_save(song, file) == 0); smf_delete(song);
    song = smf_load(file); assert(song != NULL && song->format == 1 && song->number_of_tracks == 2);
    first = smf_get_track_by_number(song, 1); second = smf_get_track_by_number(song, 2);
    assert(first != NULL && second != NULL && first->number_of_events == 2 && second->number_of_events == 2);
    event = smf_track_get_event_by_number(second, 1);
    assert(event != NULL && event->track_number == 2 && event->midi_buffer[0] == 0x91 && event->time_pulses == 120);
    assert(smf_event_is_eot(smf_track_get_event_by_number(first, 2)));
    smf_delete(song);
    puts("API case5 format-one-multitrack-roundtrip PASS");

    const unsigned char invalid_header[] = {'N','O','P','E',0,0,0,6,0,0,0,1,1,0xe0};
    assert(smf_load_from_memory(invalid_header, sizeof(invalid_header)) == NULL);
    assert(smf_event_new_from_bytes(-1, 60, 80) == NULL);
    event = smf_event_new_textual(1, "MIDI regression");
    assert(event != NULL && smf_event_is_textual(event) && smf_event_is_valid(event));
    char *text = smf_event_extract_text(event);
    assert(text != NULL && strcmp(text, "MIDI regression") == 0);
    free(text); smf_event_delete(event);
    puts("API case6 invalid-input-and-text-metadata PASS");
    puts("libsmf API cases 6/6 PASS");
    return 0;
}
LIBSMF_API_EOF

%build
# Plain original configure: do not disable the default Readline check or libraries.
%configure
%make_build
gcc %{optflags} -UNDEBUG -Isrc $(pkg-config --cflags glib-2.0) api-smoke.c -Lsrc/.libs -lsmf $(pkg-config --libs glib-2.0) -lm -o api-smoke

%install
%make_install
find %{buildroot} -name '*.la' -delete
install -Dpm0755 api-smoke %{buildroot}%{_libexecdir}/libsmf-tests/api-smoke
install -Dpm0644 api-smoke.c %{buildroot}%{_libexecdir}/libsmf-tests/api-smoke.c

%check
# Original automake check has zero runtime cases; retain it unchanged.
%make_build check
# Refuse silent fallback from the original optional-default Readline probe.
grep -Fx '#define HAVE_LIBREADLINE 1' config.h
readelf -d src/.libs/smfsh | grep -E 'NEEDED.*\[libreadline\.so\.'
test -f src/.libs/libsmf.a
(cd license-notices; sha256sum -c SHA256SUMS)
case_dir="$(mktemp -d)"
trap 'rm -rf "$case_dir"' EXIT
LD_LIBRARY_PATH="$PWD/src/.libs" ./api-smoke "$case_dir"
# install-post stripping precedes check: bind actual packaged driver bytes.
(cd %{buildroot}%{_libexecdir}/libsmf-tests; sha256sum api-smoke api-smoke.c > SHA256SUMS)

%files
%license COPYING license-notices
%doc NEWS TODO
%{_bindir}/smfsh
%{_includedir}/smf.h
%{_libdir}/libsmf.so*
%{_libdir}/libsmf.a
%{_libdir}/pkgconfig/smf.pc
%{_mandir}/man1/smfsh.1*
%{_libexecdir}/libsmf-tests

%changelog
* Sat Oct 24 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3-1
- Preserve default shared/static libraries, Readline shell and original check.
- Retain all original notices and complete GNU license texts.
- Add six strict MIDI API cases and installed physical-library bindings.
