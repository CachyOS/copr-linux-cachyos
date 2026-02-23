**FEDORA WORKSTATION**

> *sudo dnf copr enable bieszczaders/kernel-cachyos-lto*

> *sudo dnf install kernel-cachyos-lto kernel-cachyos-lto-devel-matched*

OR for LTS kernel

> *sudo dnf install kernel-cachyos-lts-lto kernel-cachyos-lts-lto-devel-matched*

LTS kernel works with x86_64v2 CPUs.

**FEDORA SILVERBLUE**

> *cd /etc/yum.repos.d/*

> *sudo wget https://copr.fedorainfracloud.org/coprs/bieszczaders/kernel-cachyos-lto/repo/fedora-$(rpm -E %fedora)/bieszczaders-kernel-cachyos-fedora-lto-$(rpm -E %fedora).repo*

> *sudo rpm-ostree override remove kernel kernel-core kernel-modules kernel-modules-core kernel-modules-extra --install kernel-cachyos-lto*

> *sudo systemctl reboot*

OR for LTS kernel

> *sudo rpm-ostree override remove kernel kernel-core kernel-modules kernel-modules-core kernel-modules-extra --install kernel-cachyos-lts-lto*

> *sudo systemctl reboot*


**OPTIONAL (HIGHLY RECOMMENDED) FOR BETTER PERFORMANCE**

> *Install [CachyOS Addons](https://copr.fedorainfracloud.org/coprs/bieszczaders/kernel-cachyos-addons/) for additional optimizations and settings.*