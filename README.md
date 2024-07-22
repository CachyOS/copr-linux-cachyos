<div align="center">
  <img src="https://github.com/CachyOS/calamares-config/blob/grub-3.2/etc/calamares/branding/cachyos/logo.png" width="64" alt="CachyOS logo"></img>
  <br/>
  <h1 align="center">CachyOS COPR Repository for Fedora</h1>
  <p align="center">Goodies from CachyOS ported to Fedora.</p>
</div>

- [List of Packages We Provide](#list-of-ported-packages)
  - [kernel-cachyos & kernel-cachyos-lts](#kernel-cachyos--kernel-cachyos-lts)


# List of Packages We Provide
## `kernel-cachyos` & `kernel-cachyos-lts`
### A port of the default `linux-cachyos` and LTS `linux-cachyos-lts` kernels for Fedora.
#### :arrow_heading_down: Features
- Choose between `GCC` and `LLVM-ThinLTO`
- Optimized for `x86-64v3` CPUs for `kernel-cachyos` and `x86-64v2` for `kernel-cachyos-lts`
- BORE scheduler with sched-ext support (sched-ext support only for `kernel-cachyos`)
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

#### Installation Instructions
Make sure your CPU supports the higher target `x86-64` architectures.
```bash
/lib64/ld-linux-x86-64.so.2 --help | grep "(supported, searched)"
```

Next, enable the COPR repository hosting the kernels.
```bash
sudo dnf copr enable bieszczaders/kernel-cachyos # For GCC built kernels
# or
sudo dnf copr enable bieszczaders/kernel-cachyos-lto # For LLVM-ThinLTO build kernels
```

Finally you can install the kernels.
```bash
sudo dnf install kernel-cachyos kernel-cachyos-devel-matched # For GCC built kernels
# or
sudo dnf install kernel-cachyos-lto kernel-cachyos-lto-devel-matched # For LLVM-ThinLTO built kernels

## LTS Kernel
sudo dnf install kernel-cachyos-lts kernel-cachyos-lts-devel-matched
# or
sudo dnf install kernel-cachyos-lts-lto kernel-cachyos-lts-lto-devel-matched
```

#### Fedora Silverblue
```bash
cd /etc/yum.repos.d/
sudo wget https://copr.fedorainfracloud.org/coprs/bieszczaders/kernel-cachyos/repo/fedora-$(rpm -E %fedora)/bieszczaders-kernel-cachyos-fedora-$(rpm -E %fedora).repo
sudo rpm-ostree override remove kernel kernel-core kernel-modules kernel-modules-core kernel-modules-extra --install kernel-cachyos
sudo systemctl reboot
```

