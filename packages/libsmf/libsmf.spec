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
Patch0:         0001-preserve-track-offsets-before-realloc.patch
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
BuildRequires:  patch
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
%setup -q -n libsmf-1.3
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
%autopatch -p1
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
cat > libsmf-lifetime.c <<'LIBSMF_LIFETIME_C_EOF'
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
/* Draft: target CI only, never compiled or executed on the local host.
 * Compile against the complete patched smf_save.c, not a copied function.
 * Moving allocations test reconstruction; they do NOT prove that original UB
 * must fail at runtime. The separate original-source GCC diagnostic is the
 * negative control, with an explicit compiler-specific claim boundary.
 */
#include <assert.h>
#include <errno.h>
#include <limits.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <smf.h>
#include "src/smf_private.h"
#if defined(malloc) || defined(realloc)
#error Unexpected configure replacement allocator in moving-realloc control
#endif

static void *live;
static size_t live_length;
static unsigned moves, multi_track_moves;
static int fail_offsets, fail_growth;
static smf_t *active;

static void *offset_malloc(size_t length)
{
    if (fail_offsets) {
        fail_offsets = 0;
        errno = ENOMEM;
        return NULL;
    }
    return malloc(length);
}

static void *moving_realloc(void *old, size_t length)
{
    assert(old == live && length > live_length);
    if (fail_growth) {
        fail_growth = 0;
        errno = ENOMEM;
        return NULL;
    }
    unsigned active_tracks = 0;
    for (int i = 1; i <= active->number_of_tracks; ++i)
        if (smf_get_track_by_number(active, i)->file_buffer != NULL)
            ++active_tracks;
    void *replacement = malloc(length);
    assert(replacement != NULL && replacement != old);
    if (old != NULL) {
        memcpy(replacement, old, live_length);
        ++moves;
        if (active_tracks >= 2)
            ++multi_track_moves;
        free(old);
    }
    live = replacement;
    live_length = length;
    return replacement;
}

#define malloc offset_malloc
#define realloc moving_realloc
#define smf_save regression_save
#define smf_event_is_eot regression_is_eot
#define smf_event_new_textual regression_new_textual
#include "src/smf_save.c"
#undef smf_event_new_textual
#undef smf_event_is_eot
#undef smf_save
#undef realloc
#undef malloc

static smf_track_t *add_track(smf_t *song)
{
    smf_track_t *track = smf_track_new();
    assert(track != NULL);
    smf_add_track(song, track);
    return track;
}

static void direct_growth(void)
{
    smf_t *song = smf_new();
    assert(song != NULL);
    active = song;
    smf_track_t *a = add_track(song), *b = add_track(song), *empty = add_track(song);
    assert(smf_extend(song, 64) != NULL);
    for (int i = 0; i < 64; ++i)
        ((unsigned char *)song->file_buffer)[i] = (unsigned char)i;
    a->file_buffer = (char *)song->file_buffer + 4;
    a->file_buffer_length = 16;
    b->file_buffer = (char *)song->file_buffer + 24;
    b->file_buffer_length = 8;
    void *before = song->file_buffer;
    fail_offsets = 1;
    assert(smf_extend(song, 7) == NULL && fail_offsets == 0);
    assert(song->file_buffer == before && song->file_buffer_length == 64);
    assert(a->file_buffer == (char *)before + 4 && b->file_buffer == (char *)before + 24);
    fail_growth = 1;
    assert(smf_extend(song, 7) == NULL && fail_growth == 0);
    assert(song->file_buffer == before && song->file_buffer_length == 64);
    assert(a->file_buffer == (char *)before + 4 && b->file_buffer == (char *)before + 24);
    for (int round = 0; round < 32; ++round) {
        int length = song->file_buffer_length;
        void *tail = smf_extend(song, 7);
        assert(tail == (char *)song->file_buffer + length);
        assert(song->file_buffer_length == length + 7);
        assert(a->file_buffer == (char *)song->file_buffer + 4 && a->file_buffer_length == 16);
        assert(b->file_buffer == (char *)song->file_buffer + 24 && b->file_buffer_length == 8);
        assert(empty->file_buffer == NULL && empty->file_buffer_length == 0);
        for (int i = 0; i < 64; ++i)
            assert(((unsigned char *)song->file_buffer)[i] == (unsigned char)i);
        memset(tail, 0xa5, 7);
    }
    /* Reject overflow before allocator invocation, retaining ownership. */
    assert(smf_extend(song, INT_MAX) == NULL);
    assert(song->file_buffer_length == 64 + 32 * 7);
    free_buffer(song);
    live = NULL;
    live_length = 0;
    smf_delete(song);
    puts("moving realloc offsets, NULL track, allocation failures and bounds PASS");
}

static void put32(unsigned char *out, unsigned value)
{
    out[0] = value >> 24; out[1] = value >> 16;
    out[2] = value >> 8; out[3] = value;
}

static void exact_file(const char *path, const unsigned char *expected, size_t length)
{
    unsigned char actual[4096];
    FILE *file = fopen(path, "rb");
    assert(file != NULL && fread(actual, 1, sizeof(actual), file) == length);
    assert(feof(file) && !ferror(file) && fclose(file) == 0);
    assert(memcmp(actual, expected, length) == 0);
}

int main(int argc, char **argv)
{
    assert(argc == 2);
    setvbuf(stdout, NULL, _IONBF, 0);
    direct_growth();
    unsigned char expected[4096] = {'M','T','h','d',0,0,0,6,0,1,0,4,0,120};
    size_t length = 14;
    smf_t *song = smf_new();
    assert(song != NULL);
    active = song;
    for (int t = 0; t < 4; ++t) {
        smf_track_t *track = add_track(song);
        memcpy(expected + length, "MTrk", 4);
        put32(expected + length + 4, 64 * 4 + 4);
        length += 8;
        for (int n = 0; n < 64; ++n) {
            smf_event_t *event = smf_event_new_from_bytes(0x90 + t, 32 + n %% 32, 64);
            assert(event != NULL);
            smf_track_add_event_pulses(track, event, n);
            expected[length++] = n == 0 ? 0 : 1;
            expected[length++] = 0x90 + t;
            expected[length++] = 32 + n %% 32;
            expected[length++] = 64;
        }
        const unsigned char eot[] = {0, 0xff, 0x2f, 0};
        memcpy(expected + length, eot, sizeof(eot));
        length += sizeof(eot);
    }
    char path[4096];
    int count = snprintf(path, sizeof(path), "%%s/moving.mid", argv[1]);
    assert(count > 0 && (size_t)count < sizeof(path));
    assert(regression_save(song, path) == 0);
    live = NULL; live_length = 0;
    exact_file(path, expected, length);
    smf_delete(song);
    song = smf_load(path);
    assert(song != NULL && song->format == 1 && song->number_of_tracks == 4 && song->ppqn == 120);
    active = song;
    for (int t = 0; t < 4; ++t) {
        smf_track_t *track = smf_get_track_by_number(song, t + 1);
        assert(track != NULL && track->number_of_events == 65);
        for (int n = 0; n < 64; ++n) {
            smf_event_t *event = smf_track_get_event_by_number(track, n + 1);
            const unsigned char bytes[] = {0x90 + t, 32 + n %% 32, 64};
            assert(event != NULL && event->time_pulses == n && event->midi_buffer_length == 3);
            assert(memcmp(event->midi_buffer, bytes, 3) == 0);
        }
        assert(smf_event_is_eot(smf_track_get_event_by_number(track, 65)));
    }
    assert(regression_save(song, path) == 0);
    live = NULL; live_length = 0;
    exact_file(path, expected, length);
    assert(moves > 1000 && multi_track_moves > 500);
    smf_delete(song);
    printf("moving realloc exact four-track wire/load/save PASS moves=%%u multi=%%u\n", moves, multi_track_moves);
    return 0;
}
LIBSMF_LIFETIME_C_EOF
cat > libsmf-lifetime.mk <<'LIBSMF_LIFETIME_MAKE_EOF'
# Draft supplemental Makefile: trusted target CI only, after configure.
# Invoke using: make -C src -f Makefile -f ../libsmf-lifetime.mk <target>
# Configured CC/DEFS/includes/GLib flags remain those of the original Makefile.
.PHONY: lifetime-fixed-diagnostic lifetime-original-diagnostic lifetime-regression
lifetime-fixed-diagnostic:
	$(CC) $(DEFS) $(DEFAULT_INCLUDES) $(INCLUDES) $(AM_CPPFLAGS) $(CPPFLAGS) $(libsmf_la_CFLAGS) $(CFLAGS) -Wuse-after-free=3 -Werror=use-after-free -x c -c smf_save.c -o ../lifetime-fixed.o

lifetime-original-diagnostic:
	@set +e; \
	$(CC) $(DEFS) $(DEFAULT_INCLUDES) $(INCLUDES) $(AM_CPPFLAGS) $(CPPFLAGS) $(libsmf_la_CFLAGS) $(CFLAGS) -Wuse-after-free=3 -Werror=use-after-free -x c -c ../license-notices/src/smf_save.c.notice -o ../lifetime-original.o > ../lifetime-original-compiler.stdout 2> ../lifetime-original-compiler.stderr; \
	compiler_status=$$?; \
	printf '%%s\n' "$$compiler_status" > ../lifetime-original-compiler.status || exit 125; \
	cat ../lifetime-original-compiler.stdout || exit 125; \
	cat ../lifetime-original-compiler.stderr >&2 || exit 125; \
	exit "$$compiler_status"

lifetime-regression:
	$(CC) $(DEFS) $(DEFAULT_INCLUDES) $(INCLUDES) $(AM_CPPFLAGS) $(CPPFLAGS) $(libsmf_la_CFLAGS) $(CFLAGS) -UNDEBUG ../libsmf-lifetime.c $(LDFLAGS) -L.libs -lsmf $(GLIB_LIBS) -lm -o ../lifetime-regression
LIBSMF_LIFETIME_MAKE_EOF
cat > libsmf-lifetime-check.sh <<'LIBSMF_LIFETIME_CHECK_EOF'
#!/usr/bin/env bash
# Unexecuted draft %%check addition: target CI only, never run locally.
# Preserve existing original check and six build/installed API cases.
set -euo pipefail
LC_ALL=C make -C src -f Makefile -f ../libsmf-lifetime.mk lifetime-fixed-diagnostic
for output in lifetime-original-compiler.stdout lifetime-original-compiler.stderr lifetime-original-compiler.status lifetime-original.o lifetime-original-diagnostic.log; do
    test ! -e "$output" && test ! -L "$output"
done
if LC_ALL=C make -C src -f Makefile -f ../libsmf-lifetime.mk lifetime-original-diagnostic > lifetime-original-diagnostic.log 2>&1; then
    cat lifetime-original-diagnostic.log
    echo 'FAIL: exact original source unexpectedly accepted by diagnostic control' >&2
    exit 1
else
    original_make_status=$?
fi
cat lifetime-original-diagnostic.log
sha256sum lifetime-original-diagnostic.log lifetime-original-compiler.stdout lifetime-original-compiler.stderr lifetime-original-compiler.status
test "$original_make_status" -eq 2
test "$(cat lifetime-original-compiler.status)" = 1
test ! -s lifetime-original-compiler.stdout
test ! -e lifetime-original.o

# Parse only actual compiler stderr, not make's wrapper exit or its command text.
# Every error/fatal-error diagnostic must be the retained causal UAF location.
# Multiple identical causal diagnostics are allowed; uniqueness is not claimed.
causal_re="^[.][.]/license-notices/src/smf_save[.]c[.]notice:77:[0-9]+: error: pointer 'previous_file_buffer' may be used after 'realloc' \\[-Werror=use-after-free\\]$"
realloc_re="^[.][.]/license-notices/src/smf_save[.]c[.]notice:65:[0-9]+: note: call to 'realloc' here$"
causal_count=0
realloc_count=0
while IFS= read -r diagnostic || [[ -n $diagnostic ]]; do
    [[ $diagnostic != *$'\033'* && $diagnostic != *$'\r'* ]]
    if [[ $diagnostic == *'error:'* ]]; then
        if [[ ! $diagnostic =~ $causal_re ]]; then
            printf 'FAIL: unexpected compiler error diagnostic: %%s\n' "$diagnostic" >&2
            exit 1
        fi
        causal_count=$((causal_count + 1))
    fi
    if [[ $diagnostic =~ $realloc_re ]]; then
        realloc_count=$((realloc_count + 1))
    fi
done < lifetime-original-compiler.stderr
test "$causal_count" -ge 1
test "$realloc_count" -ge 1
printf 'original-source GCC lifetime diagnostic negative PASS causal_errors=%%s realloc_notes=%%s compiler_exit=1 make_exit=2 (not runtime failure; not unique-diagnostic claim)\n' "$causal_count" "$realloc_count"

make -C src -f Makefile -f ../libsmf-lifetime.mk lifetime-regression
test "$#" -eq 1
moving_case_dir="$1"
LD_LIBRARY_PATH="$PWD/src/.libs" ./lifetime-regression "$moving_case_dir"
LIBSMF_LIFETIME_CHECK_EOF

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
bash ./libsmf-lifetime-check.sh "$case_dir"
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
- Preserve live track offsets before realloc and add target lifetime controls.
