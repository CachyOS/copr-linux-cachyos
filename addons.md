# **CachyOS Addons for Fedora**

# **CachyOS Settings**

Settings used in CachyOS, including modprobe configurations and udev rules, specifically packaged and optimized for Fedora.
* [GitHub CachyOS-Settings](https://github.com/CachyOS/CachyOS-Settings).

# **scx-scheds and scx-tools**

The `scx-scheds` package provides various sched-ext (BPF) schedulers. `scx-tools` includes `scxctl` for managing and monitoring these schedulers.
* [GitHub scx-scheds](https://github.com/sched-ext/scx).

# **scx-manager**

A simple and intuitive GUI for managing and switching between different sched-ext schedulers via scx_loader.
* [GitHub scx-manager](https://github.com/CachyOS/scx-manager/).

# **Ananicy-cpp**

An auto-nice daemon with CachyOS-specific rules to improve system responsiveness by automatically adjusting process priorities. Note: After further development of the sched-ext schedulers, it is usually okay to use alongside them, but can be disabled as a troubleshooting step if instability occurs.
* [GitHub ananicy-cpp](https://gitlab.com/ananicy-cpp/ananicy-cpp/).

# **Distribution and Contribution**

Developers:
* [andersrh](https://github.com/andersrh)
* [TrixieUA](https://github.com/TrixieUA)

Contributors:
* Piotr Gorski <piotrgorski@cachyos.org>
* Damian N. <nycko123@gmail.com>