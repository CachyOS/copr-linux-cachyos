
**FEDORA WORKSTATION**

> *sudo dnf copr enable bieszczaders/kernel-cachyos-addons*

INSTALL REQUIRED PACKAGES

> *sudo dnf install libcap-ng libcap-ng-devel procps-ng procps-ng-devel*

INSTALL UKSMD

> *sudo dnf install uksmd*

ENABLE SERVICE

> *sudo systemctl enable --now uksmd.service*

CHECKING THE CORRECT OPERATION OF THE UKSMD

> *uksmdstats*

**FEDORA SILVERBLUE**

> *cd /etc/yum.repos.d/*

> *sudo wget https://copr.fedorainfracloud.org/coprs/bieszczaders/kernel-cachyos-addons/repo/fedora-$(rpm -E %fedora)/bieszczaders-kernel-cachyos-addons-fedora-$(rpm -E %fedora).repo*

INSTALL REQUIRED PACKAGES

> *sudo rpm-ostree install libcap-ng-devel procps-ng-devel*

INSTALL UKSMD

> *sudo rpm-ostree install uksmd*

> *sudo systemctl reboot*

ENABLE SERVICE

> *sudo systemctl enable --now uksmd.service*

CHECKING THE CORRECT OPERATION OF THE UKSMD

> *uksmdstats*

# **Sched-ext schedulers**
The stable branch kernels have support for sched-ext schedulers. In order to use them, you need to install the package, which contains the schedulers using the following instructions:

In order to install the package, run the following command:

**FEDORA WORKSTATION**

> *sudo dnf install scx-scheds*

**FEDORA SILVERBLUE**

> *sudo rpm-ostree install scx-scheds*

On Silverblue version 39 or 40 you will also have to upgrade the libbpf package to the latest version from our repo:
> *sudo rpm-ostree override replace --experimental --from repo=copr:copr.fedorainfracloud.org:bieszczaders:kernel-cachyos-addons libbpf*

If you have previously run the above command and want to upgrade to Silverblue 41 or 42, you will need to reset the override of libbpf before the upgrade:
> *rpm-ostree override reset libbpf*

In order to run a scheduler, you can run the executable for the specific scheduler, you want. For example scx_bpfland:

> *sudo scx_bpfland*

If you want to use the systemd service, you can enable and run it, and it will also start, when the system boots:

> *sudo systemctl enable --now scx.service*

The default scheduler is scx_bpfland, but you can change it in the configuration file, which is located under /etc/default/scx