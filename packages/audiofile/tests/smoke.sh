#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- audiofile audiofile-devel
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
cat >"$d/smoke.c" <<'EOF'
#include <audiofile.h>
int main(int argc,char **argv){AFfilesetup s=afNewFileSetup();afInitFileFormat(s,AF_FILE_WAVE);AFfilehandle f=afOpenFile(argv[1],"w",s);short x[4]={0,1,-1,0};if(!f)return 1;if(afWriteFrames(f,AF_DEFAULT_TRACK,x,4)!=4)return 2;afCloseFile(f);afFreeFileSetup(s);return 0;}
EOF
gcc "$d/smoke.c" -o "$d/smoke" $(pkg-config --cflags --libs audiofile)
"$d/smoke" "$d/out.wav"
sfinfo "$d/out.wav" | grep -F '4 frames'
