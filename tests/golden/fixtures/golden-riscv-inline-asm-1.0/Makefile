# SPDX-License-Identifier: MIT
CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra

.PHONY: all clean check
all: golden-inline

golden-inline: golden_inline.c
	$(CC) $(CFLAGS) -o $@ $<

check: golden-inline
	./golden-inline | grep -E '^[0-9]+$$'

clean:
	rm -f golden-inline
