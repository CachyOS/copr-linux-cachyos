**FEDORA WORKSTATION**

> *sudo dnf copr enable bieszczaders/kernel-cachyos-addons*

INSTALL ADDON PACKAGES

> *sudo dnf install cachyos-settings scx-scheds scx-tools scx-manager ananicy-cpp*

**FEDORA SILVERBLUE**

> *cd /etc/yum.repos.d/*

> *sudo wget https://copr.fedorainfracloud.org/coprs/bieszczaders/kernel-cachyos-addons/repo/fedora-$(rpm -E %fedora)/bieszczaders-kernel-cachyos-addons-fedora-$(rpm -E %fedora).repo*

INSTALL ADDON PACKAGES

> *sudo rpm-ostree install cachyos-settings scx-scheds scx-tools ananicy-cpp*

> *sudo systemctl reboot*


# **Configuration and Usage**

**CachyOS-Settings**
To fully apply CachyOS settings, you may need to regenerate your dracut image:
> *sudo dracut -f*

**Sched-ext (scx)**
You can start a scheduler manually or via systemd. For example, to run `scx_bpfland`:
> *sudo scx_bpfland*

To enable the systemd service (defaults to scx_bpfland, configurable in `/etc/default/scx`):
> *sudo systemctl enable --now scx.service*

You can use `scxctl` to manage profiles and monitor schedulers.

**Ananicy-cpp**
To enable the auto-nice daemon:
> *sudo systemctl enable --now ananicy-cpp*

🚨 **NOTE**: After further development of the sched-ext schedulers, ananicy-cpp is usually okay to be used alongside them. However, if you experience any stalls or instability, consider disabling it as a troubleshooting step.

📖 More information is available in the [CachyOS Wiki](https://wiki.cachyos.org/configuration/sched-ext/).