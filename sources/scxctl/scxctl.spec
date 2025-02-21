%define _disable_source_fetch 0
%global _build_id_links none

Name:           scxctl
Version:        0.3.4
Release:        1%{?dist}
Summary:        A cli interface for scx_loader

License:        Apache-2.0 OR MIT
URL:            https://github.com/frap129/scxctl
Source0:        %{URL}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cargo
Requires:       scx-scheds

%description
A cli interface for scx_loader.

%prep
%setup -q

%build
export CARGO_HOME=$(pwd)/.cargo
cargo fetch
cargo build --release --offline

%install
install -Dm755 target/release/scxctl %{buildroot}%{_bindir}/scxctl

%files
%license LICENSE-APACHE LICENSE-MIT
%doc README.md
%{_bindir}/scxctl
