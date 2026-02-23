# **Official port linux-cachyos-bore and linux-cachyos-lts for Fedora**

![CachyOS](https://lingruby.ovh/images/cachyos_logo.png)

# [Meet CachyOS team!](https://cachyos.org/about/#company)

# **linux-cachyos and linux-cachyos-lts use as default the BORE-EEVDF scheduler**

* BORE - (Burst-Oriented Response Enhancer) CPU Scheduler by [firelzrd (BORE)](https://github.com/firelzrd/bore-scheduler)
* EEVDF - (Earliest Eligiable Virtual Deadline) First [EEVDF](https://lwn.net/Articles/927530) is a replacement for the CFS Scheduler from Peter Zijlstra

#**Announcement 2026/02/23: We have removed the support for prebuilt Nvidia drivers with the kernels.**
The reason for this decision is a mismatch of release schedules between RPMFusion, Fedora and CachyOS. Following this decision we advise users to switch to either RPMFusion or Negativo17's Nvidia drivers.

# **GCC-compiled kernels**
The kernels in this repository are compiled with GCC. We have a seperate repo with Clang-compiled LTO kernels, which can be found [here](https://copr.fedorainfracloud.org/coprs/bieszczaders/kernel-cachyos-lto/).

The Clang-compiled kernels give better performance, but may have issues with some kernel modules.

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

If it does not detect x86_64_v3 support do not install the default kernel. Otherwise you will end up with a non-functioning operating system!
If it detects only x86_64_v2, you can use the LTS kernel.

# **SElinux and cachyos kernel**

> *sudo setsebool -P domain_kernel_load_modules on*

If you are using SElinux. Enable the above policy to load kernel modules.