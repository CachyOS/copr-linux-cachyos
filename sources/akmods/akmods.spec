%define _disable_source_fetch 0

Name:           akmods
Version:        0.6.0
Release:        cachyos2
Summary:        Automatic kmods build and install tool

License:        MIT
URL:            http://rpmfusion.org/Packaging/KernelModules/Akmods

# We are upstream, these files are maintained directly in pkg-git
Source0:        https://github.com/1Naim/akmods/archive/refs/tags/%{version}.tar.gz
Patch0:         akmods-clang.patch

BuildArch:      noarch

BuildRequires:  help2man

# not picked up automatically
%if 0%{?rhel} == 6
Requires:       %{_bindir}/nohup
%endif
Requires:       %{_bindir}/flock
Requires:       %{_bindir}/time

# needed for actually building kmods:
Requires:       %{_bindir}/rpmdev-vercmp
Requires:       kmodtool >= 1.1-1

# needed to create CA/Keypair to sign modules
Requires:       openssl

# this should track in all stuff that is normally needed to compile modules:
Requires:       bzip2 coreutils diffutils file findutils gawk gcc grep
Requires:       gzip make sed tar unzip util-linux rpm-build

# On EL, kABI list was renamed
%if 0%{?rhel}
Requires:       (kernel-abi-stablelists if kernel-core)
%endif

# We use a virtual provide that would match either
# kernel-devel or kernel-PAE-devel
Requires:       kernel-devel-uname-r
# kernel-devel-matched enforces the same kernel version as the -devel
%if 0%{?fedora} || 0%{?rhel} >= 9
Requires:       (kernel-debug-devel-matched if kernel-debug-core)
Requires:       (kernel-devel-matched if kernel-core)
%else
Suggests:       (kernel-debug-devel if kernel-debug-core)
Suggests:       (kernel-devel if kernel-core)
%endif
Suggests:       (kernel-rt-devel if kernel-rt)

# we create a special user that used by akmods to build kmod packages
Requires(pre):  shadow-utils

# systemd unit requirements.
BuildRequires:  systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
# Optional but good to have on recent kernel
Requires: pkgconfig(libelf)

# We need grubby or systemd-boot to know the default kernel
# On EL7 assumes grubby is there by default - rhbz#2124086
%if 0%{?fedora} || 0%{?rhel} > 7
Requires: (grubby or sdubby)
%endif

%description
Akmods startup script will rebuild akmod packages during system
boot, while its background daemon will build them for kernels right
after they were installed.


%prep
%autosetup -p1 -n %{name}-%{version}
cp %{_builddir}/%{name}-%{version}/{README,README.secureboot,LICENSE} %{_builddir}


%build
# Nothing to build


%install
mkdir -p %{buildroot}%{_usrsrc}/%{name} \
         %{buildroot}%{_sbindir} \
         %{buildroot}%{_sysconfdir}/rpm \
         %{buildroot}%{_sysconfdir}/pki/%{name}/certs \
         %{buildroot}%{_sysconfdir}/pki/%{name}/private \
         %{buildroot}%{_sysconfdir}/kernel/postinst.d \
         %{buildroot}%{_sysconfdir}/logrotate.d \
         %{buildroot}%{_localstatedir}/cache/%{name} \
         %{buildroot}%{_localstatedir}/log/%{name} \
         %{buildroot}%{_tmpfilesdir}

install -pm 0755 %{_builddir}/%{name}-%{version}/akmods %{buildroot}%{_sbindir}/
install -pm 0755 %{_builddir}/%{name}-%{version}/akmodsbuild %{buildroot}%{_sbindir}/
install -pm 0755 %{_builddir}/%{name}-%{version}/akmods-ostree-post %{buildroot}%{_sbindir}/
install -pm 0644 %{_builddir}/%{name}-%{version}/akmods.log %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -pm 0640 %{_builddir}/%{name}-%{version}/cacert.config.in %{buildroot}%{_sysconfdir}/pki/%{name}/
install -pm 0755 %{_builddir}/%{name}-%{version}/akmods-kmodgenca %{buildroot}%{_sbindir}/kmodgenca
install -pm 0644 %{_builddir}/%{name}-%{version}/akmods-tmpfiles.conf %{buildroot}%{_tmpfilesdir}/%{name}.conf
install -dpm 0770 %{buildroot}%{_rundir}/%{name}/

mkdir -p %{buildroot}%{_prefix}/lib/kernel/install.d
install -pm 0755 %{_builddir}/%{name}-%{version}/95-akmodsposttrans.install %{buildroot}%{_prefix}/lib/kernel/install.d/
mkdir -p \
         %{buildroot}%{_unitdir} \
         %{buildroot}%{_presetdir}
sed "s|@SERVICE@|display-manager.service|" %{_builddir}/%{name}-%{version}/akmods.service.in >\
    %{buildroot}%{_unitdir}/akmods.service
install -pm 0644 %{_builddir}/%{name}-%{version}/95-akmods.preset %{buildroot}%{_presetdir}/
install -pm 0755 %{_builddir}/%{name}-%{version}/akmods-shutdown %{buildroot}%{_sbindir}/
install -pm 0644 %{_builddir}/%{name}-%{version}/akmods-shutdown.service %{buildroot}%{_unitdir}/
install -pm 0644 %{_builddir}/%{name}-%{version}/akmods@.service %{buildroot}%{_unitdir}/
install -pm 0644 %{_builddir}/%{name}-%{version}/akmods-keygen.target %{buildroot}%{_unitdir}/
install -pm 0644 %{_builddir}/%{name}-%{version}/akmods-keygen@.service %{buildroot}%{_unitdir}/

# Generate and install man pages.
mkdir -p %{buildroot}%{_mandir}/man1
help2man -N -i %{_builddir}/%{name}-%{version}/akmods.h2m -s 1 \
    -o %{buildroot}%{_mandir}/man1/akmods.1 \
       %{buildroot}%{_sbindir}/akmods
help2man -N -i %{_builddir}/%{name}-%{version}/akmods.h2m -s 1 \
    -o %{buildroot}%{_mandir}/man1/akmodsbuild.1 \
       %{buildroot}%{_sbindir}/akmodsbuild


%pre
# create group and user
getent group akmods >/dev/null || groupadd -r akmods
getent passwd akmods >/dev/null || \
useradd -r -g akmods -d /var/cache/akmods/ -s /sbin/nologin \
    -c "User is used by akmods to build akmod packages" akmods

%post
%systemd_post akmods.service
%systemd_post akmods@.service
%systemd_post akmods-shutdown.service

%preun
%systemd_preun akmods.service
%systemd_preun akmods@.service
%systemd_preun akmods-shutdown.service

%postun
%systemd_postun akmods.service
%systemd_postun akmods@.service
%systemd_postun akmods-shutdown.service


%files
%doc README README.secureboot
%license LICENSE
%{_sbindir}/akmodsbuild
%{_sbindir}/akmods
%{_sbindir}/akmods-ostree-post
%{_sbindir}/kmodgenca
%dir %attr(750,root,akmods) %{_sysconfdir}/pki/%{name}/certs
%dir %attr(750,root,akmods) %{_sysconfdir}/pki/%{name}/private
%config(noreplace) %attr(640,root,akmods) %{_sysconfdir}/pki/%{name}/cacert.config.in
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_unitdir}/akmods.service
%{_unitdir}/akmods@.service
%{_sbindir}/akmods-shutdown
%{_unitdir}/akmods-shutdown.service
%{_prefix}/lib/kernel/install.d/95-akmodsposttrans.install
%attr(0644,root,root) %{_unitdir}/akmods-keygen.target
%attr(0644,root,root) %{_unitdir}/akmods-keygen@.service
%dir %attr(0770,root,akmods) %{_rundir}/%{name}
%{_tmpfilesdir}/%{name}.conf
# akmods was enabled in the default preset by f28
%if 0%{?rhel}
%{_presetdir}/95-akmods.preset
%else
%exclude %{_presetdir}/95-akmods.preset
%endif
%{_usrsrc}/akmods
%dir %attr(-,akmods,akmods) %{_localstatedir}/cache/akmods
%dir %attr(0775,root,akmods) %{_localstatedir}/log/%{name}
%{_mandir}/man1/*


%changelog
%autochangelog
