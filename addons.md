# **Announcement 2024/06/16: Sched-ext schedulers support has been added to the stable branch kernels. Instructions can be found below.**

# **Userspace KSM helper daemon.**

The daemon goes through the list of userspace tasks (once per 5 seconds) and hints them to apply MADV_MERGEABLE to anonymous mappings for ksmd kthread to merge memory pages with the same content. Only long-living tasks are hinted (those that were launched more than 10 seconds ago).

This requires pmadv_ksm() syscall, which is available in [pf-kernel](https://codeberg.org/pf-kernel/linux).

# **Configuration**

The daemon requires zero configuration.

# **Distribution and Contribution**

Distributed under terms and conditions of GNU GPL v3 (only).

Developers:

* Oleksandr Natalenko <oleksandr@natalenko.name>

# **CachyOS branding**

The special version for CachyOS also includes uksmdstats .
* [GitHub uksmd](https://github.com/CachyOS/uksmd).

Contributors:

* Piotr Gorski <piotrgorski@cachyos.org>
* Damian N. <nycko123@gmail.com>