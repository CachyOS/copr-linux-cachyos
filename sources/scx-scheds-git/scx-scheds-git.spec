%global _default_patch_fuzz 2
%global commitdate 20250327
%global commit e91c87144ef7e670d124af69d8f4cab3a03f231e
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%define _disable_source_fetch 0

Name:           scx-scheds-git
Version:        1.0.10.%{commitdate}.git.%{shortcommit}
Release:        1%{?dist}
Summary:        Sched_ext Schedulers and Tools

License:        GPL=2.0
URL:            https://github.com/sched-ext/scx
Source0:        %{URL}/archive/%{commit}/scx-%{commit}.tar.gz

BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  meson >= 1.2
BuildRequires:  python
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  clang >= 17
BuildRequires:  llvm >= 17
BuildRequires:  lld >= 17
BuildRequires:  elfutils-libelf
BuildRequires:  elfutils-libelf-devel
BuildRequires:  zlib
BuildRequires:  jq
BuildRequires:  jq-devel
BuildRequires:  systemd
BuildRequires:  bpftool
Requires:  elfutils-libelf
Requires:  zlib
Requires:  jq
Obsoletes: scxctl
Conflicts: scx-scheds
Conflicts: scx_layered
Conflicts: scx_rustland
Conflicts: scx_rusty
Conflicts: scx_c_schedulers
Conflicts: rust-scx_utils-devel
Provides: scx-scheds = %{version}
Provides: scxctl = %{version}
Provides: scx_layered
Provides: scx_rustland
Provides: scx_rusty
Provides: scx_c_schedulers
Provides: rust-scx_utils-devel

%description
sched_ext is a Linux kernel feature which enables implementing kernel thread schedulers in BPF and dynamically loading them. This repository contains various scheduler implementations and support utilities.

%prep
%autosetup -p1 -n scx-%{commit}

%build
%meson \
 -Dsystemd=enabled \
 -Dopenrc=disabled \
 -Dlibalpm=disabled
%meson_build


%install
%meson_install


%files
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/default/scx
%{_bindir}/*
%{_prefix}/lib/systemd/system/scx_loader.service
%{_prefix}/lib/systemd/system/scx.service
%{_datadir}/dbus-1/system.d/org.scx.Loader.conf
%{_datadir}/dbus-1/system-services/org.scx.Loader.service


%package devel
Summary:        Development files for %{name}

%description devel
The %{name}-devel package contains libraries header files for developing applications that use %{name}

%files devel
%{_includedir}/scx/
