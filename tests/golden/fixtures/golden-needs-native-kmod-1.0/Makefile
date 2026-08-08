# SPDX-License-Identifier: GPL-2.0-only
obj-m += golden_native.o

.PHONY: all clean
all:
	$(MAKE) -C /lib/modules/$$(uname -r)/build M=$$(pwd) modules

clean:
	$(MAKE) -C /lib/modules/$$(uname -r)/build M=$$(pwd) clean
