// SPDX-License-Identifier: GPL-2.0-only
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>

static int __init golden_native_init(void)
{
    pr_info("golden-needs-native-kmod: loaded on native target kernel\n");
    return 0;
}

static void __exit golden_native_exit(void)
{
    pr_info("golden-needs-native-kmod: unloaded\n");
}

module_init(golden_native_init);
module_exit(golden_native_exit);
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Native RISC-V validation routing fixture");
