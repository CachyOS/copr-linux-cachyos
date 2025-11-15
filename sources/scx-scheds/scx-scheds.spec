%define _disable_source_fetch 0

Name:           scx-scheds
Version:        1.0.18
Release:        2%{?dist}
Summary:        Sched_ext Schedulers and Tools

License:        GPL=2.0
URL:            https://github.com/sched-ext/scx
Source0:        %{URL}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  git
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
Requires:  scx-tools
Conflicts: scx-scheds-git
Conflicts: scx_layered
Conflicts: scx_rustland
Conflicts: scx_rusty
Conflicts: rust-scx_utils-devel
Provides: scx_layered
Provides: scx_rustland
Provides: scx_rusty
Provides: rust-scx_utils-devel

%description
sched_ext is a Linux kernel feature which enables implementing kernel thread schedulers in BPF and dynamically loading them. This repository contains various scheduler implementations and support utilities.

%prep
%autosetup -n scx-%{version}


%build
export CARGO_HOME=%{_builddir}/.cargo
cargo fetch --locked
cargo build \
     --release \
     --frozen \
     --all-features \
     --workspace \
     --exclude scx_rlfifo \
     --exclude scx_mitosis \
     --exclude scx_wd40 \
     --exclude xtask \
     --exclude scxcash \
     --exclude vmlinux_docify \
     --exclude scx_arena_selftests

%install

# Install all built executables (skip .so and .d files)
find target/release \
    -maxdepth 1 -type f -executable ! -name '*.so' \
    -exec install -Dm755 -t %{buildroot}%{_bindir} {} +

%files

# Binaries
%{_bindir}/*
