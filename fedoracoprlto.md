# **Official port of linux-cachyos-lto and linux-cachyos-lts-lto for Fedora**

![CachyOS](https://lingruby.ovh/images/cachyos_logo.png)

# [Meet CachyOS team!](https://cachyos.org/about/#company)

# **linux-cachyos kernels use as default the BORE scheduler**

* BORE - (Burst-Oriented Response Enhancer) CPU Scheduler by [firelzrd (BORE)](https://github.com/firelzrd/bore-scheduler)

# **Announcement 2026/02/23: We have removed the support for prebuilt Nvidia drivers with the kernels.**
The reason for this decision is a mismatch of release schedules between RPMFusion, Fedora and CachyOS. Following this decision we advise users to switch to either RPMFusion or Negativo17's Nvidia drivers.

# **Nvidia driver 575.57.08 will likely cause a kernel panic with this kernel, if you want nvidia driver to work use gcc compiled kernel like [kernel-cachyos](https://copr.fedorainfracloud.org/coprs/bieszczaders/kernel-cachyos)**

# **Important Notice: Clang-compiled LTO Kernel Repository**
This repository offers a kernel compiled with Clang and LTO (Link-Time Optimization). It's crucial to note that enabling this repository may disrupt AKMODs functionality on kernels compiled with GCC, such as the stock Fedora kernel or kernel-cachyos (non-LTO).

# **Features**

* AMD P-State Preferred Core and AMD CPB Switch support.
* Latest BTRFS and XFS improvements & fixes.
* Latest & improved ZSTD patch-set.
* Improved BFQ Scheduler.
* Back-ported patches from `linux-next` and cherry-picked patches from Clear Linux.
* BBRv3 tcp_congestion_control.
* NTSync patched and integrated into the kernel.
* OpenRGB and ACS Override support.
* HDR Patches for AMD GPU's and gamescope.
* Default support for Steam Deck.
* Sched-ext scheduler support.
* **CachyOS Addons repository**. Additional tools and settings can be found [here](https://copr.fedorainfracloud.org/coprs/bieszczaders/kernel-cachyos-addons).

# **Checking for the cpu support**

Check support by the following the command

> */lib64/ld-linux-x86-64.so.2 --help | grep "(supported, searched)"*

If it does not detect x86_64_v3 support, do not install the default kernel. Otherwise, you will end up with a non-functioning operating system!
If it detects only x86_64_v2, you can use the LTS kernel.

# **SElinux and cachyos kernel**

> *sudo setsebool -P domain_kernel_load_modules on*

If you are using SElinux, enable the above policy to load kernel modules.