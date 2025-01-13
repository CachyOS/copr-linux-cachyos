# Maintainer: Eric Naim <dnaim@cachyos.org>

# Fedora bits
%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define _default_patch_fuzz 2
%define _disable_source_fetch 0
%define debug_package %{nil}
%undefine _auto_set_build_flags
%undefine _include_frame_pointers

# Linux Kernel Versions
%define _basekver 6.12
%define _stablekver 9
%define _rpmver %{version}-%{release}
%define _kver %{_rpmver}.%{_arch}

# Define variables for directory paths
# to be used during packaging
%define _kernel_dir /lib/modules/%{_kver}
%define _devel_dir /usr/src/kernels/%{_kver}

Name:           kernel-cachyos
Summary:        Linux BORE Cachy Sauce Kernel by CachyOS with other patches and improvements.
Version:        %{_basekver}.%{_stablekver}
Release:        cachyos5%{?dist}
License:        GPL-2.0-Only
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
BuildRequires:  redhat-rpm-config
BuildRequires:  tar
BuildRequires:  xz
BuildRequires:  zstd

Source0:        https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-%{version}.tar.xz
#Source0:       https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-%_basekver.tar.xz
Source1:        https://raw.githubusercontent.com/CachyOS/linux-cachyos/master/linux-cachyos/config

Patch0:         https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}/all/0001-cachyos-base-all.patch
Patch1:         https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}/sched/0001-bore-cachy.patch

%description
    The meta package for %{name}.

%prep
    %setup -q -n linux-%{version}
    %autopatch -p1 -v -M 9

    cp %{SOURCE1} .config

    # Must always enable configs
    scripts/config -e CACHY
    scripts/config -e SCHED_BORE
    scripts/config -d HZ_300
    scripts/config -e HZ_1000
    scripts/config --set-val HZ 1000
    scripts/config --set-val X86_64_VERSION 3
    scripts/config --set-str CONFIG_LSM lockdown,yama,integrity,selinux,bpf,landlock
    scripts/config -u DEFAULT_HOSTNAME

    make olddefconfig
    diff -u %{SOURCE1} .config || :

%build
    make %{?_smp_mflags} EXTRAVERSION=-%{release}.%{_arch} all
    make -C tools/bpf/bpftool vmlinux.h feature-clang-bpf-co-re=1

%install
    install -Dm644 "$(make -s image_name)" "%{buildroot}%{_kernel_dir}/vmlinuz"
    zstdmt -19 < Module.symvers > %{buildroot}%{_kernel_dir}/symvers.zst

    # Modules
    ZSTD_CLEVEL=19 make %{?_smp_mflags} INSTALL_MOD_PATH="%{buildroot}" INSTALL_MOD_STRIP=1 DEPMOD=/doesnt/exist modules_install

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
Requires:       gcc

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

%files


