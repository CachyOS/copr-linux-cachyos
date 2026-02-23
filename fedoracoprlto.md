# **Official port linux-cachyos-bore and linux-cachyos-lts for Fedora**

![CachyOS](https://lingruby.ovh/images/cachyos_logo.png)

# [Meet CachyOS team!](https://cachyos.org/about/#company)

# **Nvidia driver 575.57.08 will likely cause a kernel panic with this kernel, if you want nvidia driver to work use gcc compiled kernel like  [kernel-cachyos](https://copr.fedorainfracloud.org/coprs/bieszczaders/kernel-cachyos)**

# **linux-cachyos and linux-cachyos-lts use as default the BORE-EEVDF scheduler**

* BORE - (Burst-Oriented Response Enhancer) CPU Scheduler by [firelzrd (BORE)](https://github.com/firelzrd/bore-scheduler)
* EEVDF - (Earliest Eligiable Virtual Deadline) First [EEVDF](https://lwn.net/Articles/927530) is a replacement for the CFS Scheduler from Peter Zijlstra

# **Important Notice: Clang-compiled LTO Kernel Repository**

This repository offers a kernel compiled with Clang and LTO (Link-Time Optimization). It's crucial to note that enabling this repository may disrupt AKMODs functionality on kernels compiled with GCC, such as the stock Fedora kernel or kernel-cachyos (non-LTO).

Please be aware that if you activate this repository, akmods modules may not work correctly on GCC-compiled kernels. 


# **Features**

* AMD PSTATE Preferred Core and enabled as default
* Latest BTRFS and XFS improvements & fixes.
* Latest & improved ZSTD 1.5.5 patch-set.
* UserKSM daemon from pf.
* Improved BFQ Scheduler.
* Back-ported patches from `linux-next`.
* BBRv3 tcp_congestion_control.
* Scheduler patches from linux-next/tip.
* General improved sysctl settings and upstream scheduler fixes.
* OpenRGB and ACS Override support.
* HDR Patches for AMD GPU's and gamescope.
* Default support for Steam Deck.
* Sched-ext scheduler support. Installation instructions can be found [here](https://copr.fedorainfracloud.org/coprs/bieszczaders/kernel-cachyos-addons).
* [GitHub copr-linux-cachyos](https://github.com/CachyOS/copr-linux-cachyos).

# **Checking for the cpu support**

Check support by the following the command

> */lib64/ld-linux-x86-64.so.2 --help | grep "(supported, searched)"*

If it does not detect x86_64_v3 support do not install the kernel. Otherwise you will end up with a non-functioning operating system!

# **SElinux and cachyos kernel**

> *sudo setsebool -P domain_kernel_load_modules on*

If you are using SElinux. Enable the above policy to load kernel modules.