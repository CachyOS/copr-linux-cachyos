%global _default_patch_fuzz 2
%global commitdate 20251111
%global commit 6ddcb07bcdab8d2451f7543e4f98180e677c7b21
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%define _disable_source_fetch 0

Name:           scx-scheds-git
Version:        1.0.18.%{commitdate}.git.%{shortcommit}
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
BuildRequires:  protobuf-compiler
BuildRequires:  libseccomp-devel
Requires:  elfutils-libelf
Requires:  libseccomp
Requires:  protobuf
Requires:  zlib
Requires:  jq
Conflicts: scx-scheds
Conflicts: scx_layered
Conflicts: scx_rustland
Conflicts: scx_rusty
Conflicts: scx_c_schedulers
Conflicts: rust-scx_utils-devel
Provides: scx-scheds = %{version}
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
 -Dforce_meson=true \
 -Dsystemd=enabled \
 -Dopenrc=disabled
%meson_build


%install
%meson_install


%files
%{_bindir}/*

%package devel
Summary:        Development files for %{name}

%description devel
The %{name}-devel package contains libraries header files for developing applications that use %{name}

%files devel
%{_includedir}/scx/
