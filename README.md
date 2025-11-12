<div align="center">
  <img src="https://github.com/CachyOS/calamares-config/blob/grub-3.2/etc/calamares/branding/cachyos/logo.png" width="64" alt="CachyOS logo"></img>
  <br/>
  <h1 align="center">CachyOS COPR Repository for Fedora</h1>
  <p align="center">Goodies from CachyOS ported to Fedora.</p>
</div>

This repository is maintained by [@andersrh](https://github.com/andersrh) and [@TrixieUA](https://github.com/TrixieUA).

- [Kernels](#-kernels)
  - [Features](#-features)
  - [Installation Instructions](#%EF%B8%8F-installation-instructions)
    - [Default Kernel](#default-kernel)
- [Addons](#-addons)
  - [CachyOS-Settings](#cachyos-settings)
  - [scx-scheds](#scx-scheds)
  - [scx-manager](#scx-manager)
  - [ananicy-cpp](#ananicy-cpp)

# 🐧 Kernels

We offer a variety of CachyOS kernels ported to Fedora:
- `kernel-cachyos` - 1000 Hz kernel with BORE scheduler
- `kernel-cachyos-lts` - LTS kernel with BORE scheduler
- `kernel-cachyos-rt` - Real-time kernel with BORE scheduler
- `kernel-cachyos-server` - 300 Hz kernel with default EEVDF scheduler

For Fedora Workstation and Silverblue we recommend `kernel-cachyos` and for Fedora Server, Cloud and CoreOS we recommend `kernel-cachyos-server`. The LTS and Real-time kernels are for special use cases (think embedded systems) and are not recommended unless your application requires them.

## 🌟 Features
- Choose between `GCC` and `LLVM-ThinLTO`
- Optimized for `x86-64v3` CPUs for `kernel-cachyos` and `x86-64v2` for `kernel-cachyos-lts` and `kernel-cachyos-server`
- BORE scheduler with sched-ext support (excl. `kernel-cachyos-server`, sched-ext support only for `kernel-cachyos`)
- AMD P-State Preferred Core, AMD CPB Switch and upstream `amd-pstate` enchancements (exclusive to `kernel-cachyos`)
- Cachy Sauce - Provides tweaks for the scheduler and other settings
- Prebuilt `nvidia-open` kernel modules
- Latest & improved ZSTD patchset
- Improved BFQ Scheduler
- BBRv3 tcp_congestion_control
- v4l2loopback modules as default included
- Cherry picked patches from Clear Linux
- Backported patches from `linux-next`
- OpenRGB and ACS Override support
- NTSync patched and integrated into the kernel (exclusive to `kernel-cachyos`)

## ⬇️ Installation Instructions
Make sure your CPU supports the higher target `x86-64` architectures. You need minimum `x86-64-v3` for all kernels, except `kernel-cachyos-lts` and `kernel-cachyos-server` that only require `x86-64-v2`.
```bash
/lib64/ld-linux-x86-64.so.2 --help | grep "(supported, searched)"
```

Next, enable the COPR repository hosting the kernels.
```bash
sudo dnf copr enable bieszczaders/kernel-cachyos # For GCC built kernels
# or
sudo dnf copr enable bieszczaders/kernel-cachyos-lto # For LLVM-ThinLTO build kernels
```

Now you can install the kernels
```bash
sudo dnf install kernel-cachyos kernel-cachyos-devel-matched # For GCC built kernels
# or
sudo dnf install kernel-cachyos-lto kernel-cachyos-lto-devel-matched # For LLVM-ThinLTO built kernels

## LTS Kernel
sudo dnf install kernel-cachyos-lts kernel-cachyos-lts-devel-matched
# or
sudo dnf install kernel-cachyos-lts-lto kernel-cachyos-lts-lto-devel-matched

## Real-time Kernel
sudo dnf install kernel-cachyos-rt kernel-cachyos-rt-devel-matched

## Server Kernel
sudo dnf install kernel-cachyos-server kernel-cachyos-server-devel-matched
```

🚨 Lastly if you use SELinux, you need to enable the necessary policy to be able to load kernel modules.
```bash
sudo setsebool -P domain_kernel_load_modules on
```

### Fedora Silverblue
```bash
cd /etc/yum.repos.d/
sudo wget https://copr.fedorainfracloud.org/coprs/bieszczaders/kernel-cachyos/repo/fedora-$(rpm -E %fedora)/bieszczaders-kernel-cachyos-fedora-$(rpm -E %fedora).repo
sudo rpm-ostree override remove kernel kernel-core kernel-modules kernel-modules-core kernel-modules-extra --install kernel-cachyos
sudo systemctl reboot
```

### Default Kernel
By default Fedora will use the kernel that was most recently updated by `dnf` which will lead to inconsistent behaviour if you have multiple kernels installed, but we can tell Fedora to always boot with the latest CachyOS kernel by running a script after kernel updates.

Create a file in `/etc/kernel/postinst.d`:
```bash
sudo nano /etc/kernel/postinst.d/99-default
```

Enter the following content that will set the latest CachyOS kernel as the default kernel:
```bash
#!/bin/sh

set -e

grubby --set-default=/boot/$(ls /boot | grep vmlinuz.*cachy | sort -V | tail -1)
```

Make `root` the owner and make the script executable:
```bash
sudo chown root:root /etc/kernel/postinst.d/99-default ; sudo chmod u+rx /etc/kernel/postinst.d/99-default
```

The next time any installed kernel (e.g. the official Fedora kernel) gets an update, the system will change default kernel back to the latest CachyOS kernel. This way you can keep the official kernel as a backup in case an update goes wrong and you need to temporarily switch to the official kernel.

# 🧩 Addons
We provide a few addons that supplement the kernel packages and system.
- [CachyOS-Settings](https://github.com/CachyOS/CachyOS-Settings) - Settings used in CachyOS (includes modprobe config, udev rules, etc) packaged for Fedora.
- [scx-scheds](https://github.com/sched-ext/scx) - sched-ext schedulers. Provides both `scx-scheds` releases and `scx-scheds-git` package.
- [scx-manager](https://github.com/CachyOS/scx-manager/) - Simple GUI for managing sched-ext schedulers via scx_loader.
- [ananicy-cpp](https://gitlab.com/ananicy-cpp/ananicy-cpp/) & [cachyos-ananicy-rules](https://github.com/CachyOS/ananicy-rules) - Auto nice daemon with rules support.

## ⬇️ Installation instructions
First, enable the COPR repository hosting addon packages.
```bash
sudo dnf copr enable bieszczaders/kernel-cachyos-addons
```

Now you can install the addon packages.

### CachyOS-Settings
```bash
sudo dnf swap zram-generator-defaults cachyos-settings
sudo dracut -f
```

### scx-scheds
```bash
sudo dnf install scx-scheds scx-tools
#or
sudo dnf install scx-scheds-git scx-tools-git # For -git package

```
You can use [scxctl](https://github.com/sched-ext/scx-loader/blob/main/crates/scxctl/README.md) to start/change the scheduler with profiles/custom flags.

📖 Usage guide available in the [CachyOS wiki](https://wiki.cachyos.org/configuration/sched-ext/).

### scx-manager

```
sudo dnf install scx-manager
```

### ananicy-cpp

> [It is advised against running `ananicy-cpp` and a scheduler from the `sched-ext` framework *simultaneously*. Use one but not the other.](https://wiki.cachyos.org/configuration/sched-ext/#disable-ananicy-cpp)

```bash
sudo dnf install ananicy-cpp
sudo systemctl enable --now ananicy-cpp
```
