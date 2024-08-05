%global _default_patch_fuzz 2
%global commitdate 20240805
%global commit 38efa974a8c7907d40ff63fabd5510e06f2d98af
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%define _disable_source_fetch 0

Name:           scx-scheds-git
Version:        1.0.1
Release:        1.%{commitdate}.git.%{shortcommit}%{?dist}
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
Requires:  elfutils-libelf
Requires:  zlib
Requires:  jq
Conflicts: scx-scheds
Obsoletes: sched-ext-scx-git

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
%{_prefix}/lib/systemd/system/scx.service
%{_sysconfdir}/systemd/journald@sched-ext.conf
