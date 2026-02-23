**FEDORA WORKSTATION**

> *sudo dnf copr enable bieszczaders/kernel-cachyos-addons*

INSTALL ADDON PACKAGES

**CachyOS-Settings**
> *sudo dnf swap zram-generator-defaults cachyos-settings*

> *sudo dracut -f*

**scx-scheds and scx-tools**
> *sudo dnf install scx-scheds scx-tools*

**scx-manager**
> *sudo dnf install scx-manager*

**ananicy-cpp**
> *sudo dnf install ananicy-cpp*

**FEDORA SILVERBLUE**

> *cd /etc/yum.repos.d/*

> *sudo wget https://copr.fedorainfracloud.org/coprs/bieszczaders/kernel-cachyos-addons/repo/fedora-$(rpm -E %fedora)/bieszczaders-kernel-cachyos-addons-fedora-$(rpm -E %fedora).repo*

INSTALL ADDON PACKAGES

> *sudo rpm-ostree install scx-scheds scx-tools*

> *sudo systemctl reboot*


# **Configuration and Usage**

**Sched-ext (scx)**

You can use `scxctl` to start/change the scheduler with profiles/custom flags. To see all available options, run:

> *scxctl --help*

**Ananicy-cpp**

To enable the auto-nice daemon:
> *sudo systemctl enable --now ananicy-cpp*

🚨 **NOTE**: After further development of the sched-ext schedulers, ananicy-cpp is usually okay to be used alongside them. However, if you experience any stalls or instability, consider disabling it as a troubleshooting step.

📖 More information is available in the [CachyOS Wiki](https://wiki.cachyos.org/configuration/sched-ext/).