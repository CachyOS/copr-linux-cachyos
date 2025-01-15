# Maintainer: Eric Naim <dnaim@cachyos.org>

# Fedora bits
%define __spec_install_post %{__os_install_post}
%define _default_patch_fuzz 2
%define _disable_source_fetch 0
%define debug_package %{nil}
%define make_build make %{?_build_args} %{?_smp_mflags}
%undefine __brp_mangle_shebangs
%undefine _auto_set_build_flags
%undefine _include_frame_pointers

# Linux Kernel Versions
%define _basekver 6.12
%define _stablekver 9
%define _rpmver %{version}-%{release}
%define _kver %{_rpmver}.%{_arch}

%if %{_stablekver} == 0
    %define _tarkver %{_basekver}
%else
    %define _tarkver %{version}
%endif

# Build a minimal a kernel via modprobed.db
# file to reduce build times.
%define _build_minimal 0

# Builds the kernel with clang and enables
# ThinLTO
%define _build_lto 0

# Builds nvidia-open kernel modules with
# the kernel.
%define _build_nv 1
%define _nv_ver 565.77
%define _nv_pkg open-gpu-kernel-modules-%{_nv_ver}

# Define the tickrate used by the kernel
# Valid values: 100, 250, 300, 500, 600, 750 and 1000
# An invalid value will not fail and continue to use
# 1000Hz tickrate.
%define _hz_tick 1000

# Define variables for directory paths
# to be used during packaging
%define _kernel_dir /lib/modules/%{_kver}
%define _devel_dir /usr/src/kernels/%{_kver}

%if %{_build_lto}
    # Define build environment variables to build the kernel with clang
    %define _build_args CC=clang CXX=clang++ LD=ld.lld LLVM=1 LLVM_IAS=1
    %define _is_lto 1
%endif

%define _module_args KERNEL_UNAME=%{_kver} IGNORE_PREEMPT_RT_PRESENCE=1 SYSSRC=%{_builddir}/linux-%{_tarkver} SYSOUT=%{_builddir}/linux-%{_tarkver}

Name:           kernel-cachyos%{?_is_lto:-lto}
Summary:        Linux BORE %{?_is_lto:+ LTO }Cachy Sauce Kernel by CachyOS with other patches and improvements.
Version:        %{_basekver}.%{_stablekver}
Release:        cachyos8%{?_is_lto:.lto}%{?dist}
License:        GPL-2.0-only
URL:            https://cachyos.org

Requires:       kernel-core-uname-r = %{_kver}
Requires:       kernel-modules-uname-r = %{_kver}
Requires:       kernel-modules-core-uname-r = %{_kver}
Provides:       installonlypkg(kernel)
Provides:       kernel-uname-r = %{_kver}

BuildRequires:  bc
BuildRequires:  bison
BuildRequires:  cpio
BuildRequires:  dwarves
BuildRequires:  elfutils-devel
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  kernel-rpm-macros
BuildRequires:  kmod
BuildRequires:  make
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  perl-Carp
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  python3-devel
BuildRequires:  python3-pyyaml
BuildRequires:  python-srpm-macros
BuildRequires:  redhat-rpm-config
BuildRequires:  tar
BuildRequires:  xz
BuildRequires:  zstd

%if %{_build_lto}
BuildRequires:  clang
BuildRequires:  lld
BuildRequires:  llvm
%endif

%if %{_build_nv}
BuildRequires:  gcc-c++
%endif

# Indexes 0-9 are reserved for the kernel. 10-19 will be reserved for NVIDIA
Source0:        https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-%{_tarkver}.tar.xz
Source1:        https://raw.githubusercontent.com/CachyOS/linux-cachyos/master/linux-cachyos/config

%if %{_build_minimal}
# The default modprobed.db provided is used for linux-cachyos CI.
# This should not be used for production and ideally should only be used for compile tests.
# Note that any modprobed.db file is accepted
Source2:        https://raw.githubusercontent.com/CachyOS/linux-cachyos/master/modprobed.db
%endif

%if %{_build_nv}
Source10:       https://github.com/NVIDIA/open-gpu-kernel-modules/archive/%{_nv_ver}/%{_nv_pkg}.tar.gz
%endif

Patch0:         https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}/all/0001-cachyos-base-all.patch
Patch1:         https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}/sched/0001-bore-cachy.patch

%if %{_build_lto}
Patch2:         https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}/misc/dkms-clang.patch
%endif

%if %{_build_nv}
Patch10:        https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}/misc/nvidia/0001-Make-modeset-and-fbdev-default-enabled.patch
Patch11:        https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}/misc/nvidia/0002-Do-not-error-on-unkown-CPU-Type-and-add-Zen5-support.patch
Patch12:        https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}/misc/nvidia/0004-silence-event-assert-until-570.patch
Patch13:        https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}/misc/nvidia/0005-nvkms-Sanitize-trim-ELD-product-name-strings.patch
%endif

%description
    The meta package for %{name}.

%prep
    %if %{_build_nv}
        %setup -q -b 10 -n linux-%{_tarkver}
    %else
        %setup -q -n linux-%{_tarkver}
    %endif

    %autopatch -p1 -v -M 9

    cp %{SOURCE1} .config

    # Must always enable configs
    scripts/config -e CACHY
    scripts/config -e SCHED_BORE
    scripts/config --set-val X86_64_VERSION 3
    scripts/config --set-str CONFIG_LSM lockdown,yama,integrity,selinux,bpf,landlock
    scripts/config -u DEFAULT_HOSTNAME

    case %{_hz_tick} in
        100|250|300|500|600|750|1000)
            scripts/config -e HZ_%{_hz_tick} --set-val HZ %{_hz_tick};;
        *)
            echo "Invalid tickrate value, using default 1000"
            scripts/config -e HZ_1000 --set-val HZ 1000;;
    esac

    %if %{_build_lto}
        scripts/config -e LTO_CLANG_THIN
    %endif

    %if %{_build_minimal}
        %make_build LSMOD=%{SOURCE2} localmodconfig
    %endif

    %make_build olddefconfig
    diff -u %{SOURCE1} .config || :

    %if %{_build_nv}
        cd %{_builddir}/%{_nv_pkg}/kernel-open
        %patch -P 10 -p1
        cd ..
        %autopatch -p1 -v -m 11 -M 19
    %endif

%build
    %make_build EXTRAVERSION=-%{release}.%{_arch} all
    %make_build -C tools/bpf/bpftool vmlinux.h feature-clang-bpf-co-re=1

    %if %{_build_nv}
        cd %{_builddir}/%{_nv_pkg}
        CFLAGS= CXXFLAGS= LDFLAGS= %make_build %{_module_args} IGNORE_CC_MISMATCH=yes modules
    %endif

%install
    install -Dm644 "$(%make_build -s image_name)" "%{buildroot}%{_kernel_dir}/vmlinuz"
    zstdmt -19 < Module.symvers > %{buildroot}%{_kernel_dir}/symvers.zst

    # Modules
    ZSTD_CLEVEL=19 %make_build INSTALL_MOD_PATH="%{buildroot}" INSTALL_MOD_STRIP=1 DEPMOD=/doesnt/exist modules_install

    # -devel files
    install -Dt %{buildroot}%{_devel_dir} -m644 .config Makefile Module.symvers System.map tools/bpf/bpftool/vmlinux.h
    cp .config %{buildroot}%{_kernel_dir}/config
    cp System.map %{buildroot}%{_kernel_dir}/System.map
    cp --parents `find  -type f -name "Makefile*" -o -name "Kconfig*"` %{buildroot}%{_devel_dir}
    rm -rf %{buildroot}%{_devel_dir}/scripts
    rm -rf %{buildroot}%{_devel_dir}/include
    cp -a scripts %{buildroot}%{_devel_dir}
    rm -rf %{buildroot}%{_devel_dir}/scripts/tracing
    rm -f %{buildroot}%{_devel_dir}/scripts/spdxcheck.py

    # The cp commands below are needed for parity with Fedora's packaging
    # Install files that are needed for `make scripts` to succeed
    cp -a --parents security/selinux/include/classmap.h %{buildroot}%{_devel_dir}
    cp -a --parents security/selinux/include/initial_sid_to_string.h %{buildroot}%{_devel_dir}
    cp -a --parents tools/include/tools/be_byteshift.h %{buildroot}%{_devel_dir}
    cp -a --parents tools/include/tools/le_byteshift.h %{buildroot}%{_devel_dir}

    # Install files that are needed for `make prepare` to succeed -- Generic
    cp -a --parents tools/include/linux/compiler* %{buildroot}%{_devel_dir}
    cp -a --parents tools/include/linux/types.h %{buildroot}%{_devel_dir}
    cp -a --parents tools/build/Build.include %{buildroot}%{_devel_dir}
    cp --parents tools/build/fixdep.c %{buildroot}%{_devel_dir}
    cp --parents tools/objtool/sync-check.sh %{buildroot}%{_devel_dir}
    cp -a --parents tools/bpf/resolve_btfids %{buildroot}%{_devel_dir}

    cp --parents security/selinux/include/policycap_names.h %{buildroot}%{_devel_dir}
    cp --parents security/selinux/include/policycap.h %{buildroot}%{_devel_dir}

    cp -a --parents tools/include/asm %{buildroot}%{_devel_dir}
    cp -a --parents tools/include/asm-generic %{buildroot}%{_devel_dir}
    cp -a --parents tools/include/linux %{buildroot}%{_devel_dir}
    cp -a --parents tools/include/uapi/asm %{buildroot}%{_devel_dir}
    cp -a --parents tools/include/uapi/asm-generic %{buildroot}%{_devel_dir}
    cp -a --parents tools/include/uapi/linux %{buildroot}%{_devel_dir}
    cp -a --parents tools/include/vdso %{buildroot}%{_devel_dir}
    cp --parents tools/scripts/utilities.mak %{buildroot}%{_devel_dir}
    cp -a --parents tools/lib/subcmd %{buildroot}%{_devel_dir}
    cp --parents tools/lib/*.c %{buildroot}%{_devel_dir}
    cp --parents tools/objtool/*.[ch] %{buildroot}%{_devel_dir}
    cp --parents tools/objtool/Build %{buildroot}%{_devel_dir}
    cp --parents tools/objtool/include/objtool/*.h %{buildroot}%{_devel_dir}
    cp -a --parents tools/lib/bpf %{buildroot}%{_devel_dir}
    cp --parents tools/lib/bpf/Build %{buildroot}%{_devel_dir}

    # Misc headers
    cp -a --parents arch/x86/include %{buildroot}%{_devel_dir}
    cp -a --parents tools/arch/x86/include %{buildroot}%{_devel_dir}
    cp -a include %{buildroot}%{_devel_dir}/include
    cp -a sound/soc/sof/sof-audio.h %{buildroot}%{_devel_dir}/sound/soc/sof
    cp -a tools/objtool/objtool %{buildroot}%{_devel_dir}/tools/objtool/
    cp -a tools/objtool/fixdep %{buildroot}%{_devel_dir}/tools/objtool/

    # Install files that are needed for `make prepare` to succeed -- for x86_64
    cp -a --parents arch/x86/entry/syscalls/syscall_32.tbl %{buildroot}%{_devel_dir}
    cp -a --parents arch/x86/entry/syscalls/syscall_64.tbl %{buildroot}%{_devel_dir}
    cp -a --parents arch/x86/tools/relocs_32.c %{buildroot}%{_devel_dir}
    cp -a --parents arch/x86/tools/relocs_64.c %{buildroot}%{_devel_dir}
    cp -a --parents arch/x86/tools/relocs.c %{buildroot}%{_devel_dir}
    cp -a --parents arch/x86/tools/relocs_common.c %{buildroot}%{_devel_dir}
    cp -a --parents arch/x86/tools/relocs.h %{buildroot}%{_devel_dir}
    cp -a --parents arch/x86/purgatory/purgatory.c %{buildroot}%{_devel_dir}
    cp -a --parents arch/x86/purgatory/stack.S %{buildroot}%{_devel_dir}
    cp -a --parents arch/x86/purgatory/setup-x86_64.S %{buildroot}%{_devel_dir}
    cp -a --parents arch/x86/purgatory/entry64.S %{buildroot}%{_devel_dir}
    cp -a --parents arch/x86/boot/string.h %{buildroot}%{_devel_dir}
    cp -a --parents arch/x86/boot/string.c %{buildroot}%{_devel_dir}
    cp -a --parents arch/x86/boot/ctype.h %{buildroot}%{_devel_dir}

    cp -a --parents scripts/syscalltbl.sh %{buildroot}%{_devel_dir}
    cp -a --parents scripts/syscallhdr.sh %{buildroot}%{_devel_dir}

    cp -a --parents tools/arch/x86/include/asm %{buildroot}%{_devel_dir}
    cp -a --parents tools/arch/x86/include/uapi/asm %{buildroot}%{_devel_dir}
    cp -a --parents tools/objtool/arch/x86/lib %{buildroot}%{_devel_dir}
    cp -a --parents tools/arch/x86/lib/ %{buildroot}%{_devel_dir}
    cp -a --parents tools/arch/x86/tools/gen-insn-attr-x86.awk %{buildroot}%{_devel_dir}
    cp -a --parents tools/objtool/arch/x86/ %{buildroot}%{_devel_dir}

    # Final cleanups ala Fedora
    find %{buildroot}%{_devel_dir}/scripts \( -iname "*.o" -o -iname "*.cmd" \) -exec rm -f {} +
    find %{buildroot}%{_devel_dir}/tools \( -iname "*.o" -o -iname "*.cmd" \) -exec rm -f {} +
    touch -r %{buildroot}%{_devel_dir}/Makefile \
        %{buildroot}%{_devel_dir}/include/generated/uapi/linux/version.h \
        %{buildroot}%{_devel_dir}/include/config/auto.conf

    # These links will be owned by the modules package, creating a broken
    # link unless the -devel package is installed. why??
    rm -rf %{buildroot}%{_kernel_dir}/build
    ln -s %{_devel_dir} %{buildroot}%{_kernel_dir}/build
    ln -s %{_kernel_dir}/build %{buildroot}%{_kernel_dir}/source

    # Create stub initramfs to inflate disk space requirements.
    # This should hopefully prevent some initramfs failures due to
    # insufficient space in /boot (#bz #530778)
    # 90 seems to be a safe value nowadays. It is slightly inflated than the
    # measured average to also account for installed vmlinuz in /boot
    install -dm755 %{buildroot}/boot
    dd if=/dev/zero of=%{buildroot}/boot/initramfs-%{_kver}.img bs=1M count=90

    %if %{_build_nv}
        cd %{_builddir}/%{_nv_pkg}
        install -Dt %{buildroot}%{_kernel_dir}/nvidia -m644 kernel-open/*.ko
        find %{buildroot}%{_kernel_dir}/nvidia -name '*.ko' -exec zstd --rm -19 {} +
        install -Dt %{buildroot}/usr/share/licenses/%{name}-nvidia-open -m644 COPYING
    %endif

%package core
Summary:        Linux BORE Cachy Sauce Kernel by CachyOS with other patches and improvements
Provides:       kernel-core-uname-r = %{_kver}
Provides:       installonlypkg(kernel)
Requires:       kernel-modules-uname-r = %{_kver}
Requires:       coreutils
Requires:       dracut
Requires:       kmod

%description core
    The kernel package contains the Linux kernel (vmlinuz), the core of any
    Linux operating system.  The kernel handles the basic functions
    of the operating system: memory allocation, process allocation, device
    input and output, etc.

%post core
    mkdir -p %{_localstatedir}/lib/rpm-state/%{name}
    touch %{_localstatedir}/lib/rpm-state/%{name}/installing_core_%{_kver}

%posttrans core
    rm -f %{_localstatedir}/lib/rpm-state/%{name}/installing_core_%{_kver}
    /bin/kernel-install add %{_kver} %{_kernel_dir}/vmlinuz || exit $?
    if [[ ! -e "/boot/symvers-%{_kver}.zst" ]]; then
        cp "%{_kernel_dir}/symvers.zst" "/boot/symvers-%{_kver}.zst"
        if command -v restorecon &>/dev/null; then
            restorecon "/boot/symvers-%{_kver}.zst"
        fi
    fi

%preun core
    /bin/kernel-install remove %{_kver} || exit $?
    if [ -x /usr/sbin/weak-modules ]; then
        /usr/sbin/weak-modules --remove-kernel %{_kver} || exit $?
    fi

%files core
    %dir %{_kernel_dir}
    %license COPYING
    %ghost /boot/initramfs-%{_kver}.img
    %{_kernel_dir}/vmlinuz
    %{_kernel_dir}/modules.builtin
    %{_kernel_dir}/modules.builtin.modinfo
    %{_kernel_dir}/symvers.zst
    %{_kernel_dir}/config
    %{_kernel_dir}/System.map

%package modules
Summary:        Kernel modules package for %{name}.
Provides:       kernel-modules-uname-r = %{_kver}
Provides:       kernel-modules-core-uname-r = %{_kver}
Provides:       installonlypkg(kernel-module)
Requires:       kernel-uname-r = %{_kver}

%description modules
    This package provides kernel modules for the %{name}-core kernel package.

%post modules
    /sbin/depmod -a %{_kver}
    if [ ! -f %{_localstatedir}/lib/rpm-state/%{name}/installing_core_%{_kver} ]; then
        mkdir -p %{_localstatedir}/lib/rpm-state/%{name}
        touch %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{_kver}
    fi

%posttrans modules
    if [ -f %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{_kver} ]; then
        rm -f %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{_kver}
        echo "Running: dracut -f --kver %{_kver}"
        dracut -f --kver "%{_kver}" || exit $?
    fi

%postun modules
    /sbin/depmod -a %{_kver}

%files modules
    %{_kernel_dir}/modules.order
    %{_kernel_dir}/build
    %{_kernel_dir}/source
    %{_kernel_dir}/kernel

%package devel
Summary:        Development package for building kernel modules to match %{name}
Provides:       kernel-devel-uname-r = %{_kver}
Provides:       installonlypkg(kernel)
AutoReqProv:    no
Requires(pre):  findutils
Requires:       findutils
Requires:       perl-interpreter
Requires:       openssl-devel
Requires:       elfutils-libelf-devel
Requires:       bison
Requires:       flex
Requires:       make

%if %{_build_lto}
Requires:       clang
Requires:       lld
Requires:       llvm
%else
Requires:       gcc
%endif

%description devel
    This package provides kernel headers and makefiles sufficient to build modules against %{name}.

%post devel
    if [ -f /etc/sysconfig/kernel ]; then
        . /etc/sysconfig/kernel || exit $?
    fi
    if [ "$HARDLINK" != "no" -a -x /usr/bin/hardlink -a ! -e /run/ostree-booted ]; then
        (cd /usr/src/kernels/%{_kver} &&
        /usr/bin/find . -type f | while read f; do
            hardlink -c /usr/src/kernels/*%{?dist}.*/$f $f > /dev/null
        done;
        )
    fi

%files devel
    %{_devel_dir}

%package devel-matched
Summary:        Meta package to install matching core and devel packages for %{name}
Provides:       kernel-devel-matched = %{_rpmver}
Requires:       %{name}-core = %{_rpmver}
Requires:       %{name}-devel = %{_rpmver}

%description devel-matched
    This meta package is used to install matching core and devel packages for %{name}.

%files devel-matched

%if %{_build_nv}
%package nvidia-open
Summary:        nvidia-open %{_nv_ver} kernel modules for %{name}
Provides:       nvidia-kmod >= %{_nv_ver}
Provides:       installonlypkg(kernel-module)
Requires:       kernel-uname-r = %{_kver}
Conflicts:      akmod-nvidia
Recommends:     xorg-x11-drv-nvidia >= %{_nv_ver}

%description nvidia-open
    This package provides nvidia-open %{_nv_ver} kernel modules for %{name}.

%post nvidia-open
    /sbin/depmod -a %{_kver}

%files nvidia-open
    %license /usr/share/licenses/%{name}-nvidia-open/COPYING
    %{_kernel_dir}/nvidia
%endif

%files


