**FEDORA WORKSTATION**

> *sudo dnf copr enable bieszczaders/kernel-cachyos*

> *sudo dnf install kernel-cachyos kernel-cachyos-devel-matched*

OR for realtime kernel

>*sudo dnf install kernel-cachyos-rt kernel-cachyos-rt-devel-matched*

OR for LTS kernel
>*sudo dnf install kernel-cachyos-lts kernel-cachyos-lts-devel-matched*

LTS kernel works with x86_64v2 cpu's and legacy nvidia drivers

 **FEDORA SILVERBLUE**

> *cd /etc/yum.repos.d/*

> *sudo wget https://copr.fedorainfracloud.org/coprs/bieszczaders/kernel-cachyos/repo/fedora-$(rpm -E %fedora)/bieszczaders-kernel-cachyos-fedora-$(rpm -E %fedora).repo*

> *sudo rpm-ostree override remove kernel kernel-core kernel-modules kernel-modules-core kernel-modules-extra --install kernel-cachyos*

> *sudo systemctl reboot*

OR for realtime kernel

> *sudo rpm-ostree override remove kernel kernel-core kernel-modules kernel-modules-core kernel-modules-extra --install kernel-cachyos-rt*

> *sudo systemctl reboot*

OR for LTS kernel

>*sudo rpm-ostree override remove kernel kernel-core kernel-modules kernel-modules-core kernel-modules-extra --install  kernel-cachyos-lts*

> *sudo systemctl reboot*

LTS kernel works with x86_64v2 cpu's and legacy nvidia drivers


**OPTIONAL (HIGHLY RECOMMENDED) FOR BETTER PERFORMANCE**

> *Install [UKSMD](https://copr.fedorainfracloud.org/coprs/bieszczaders/kernel-cachyos-addons/).*