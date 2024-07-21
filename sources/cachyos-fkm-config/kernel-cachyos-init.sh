#!/bin/bash

YUM_CHANGED=false
KERNEL_CACHYOS_REPO_FILE='/etc/yum.repos.d/_copr:copr.fedorainfracloud.org:bieszczaders:kernel-cachyos.repo'
KERNEL_CACHYOS_ADDONS_REPO_FILE='/etc/yum.repos.d/_copr:copr.fedorainfracloud.org:bieszczaders:kernel-cachyos-addons.repo'

if [ ! -f $KERNEL_CACHYOS_REPO_FILE ]
then
  wget https://copr.fedorainfracloud.org/coprs/bieszczaders/kernel-cachyos/repo/fedora-$(rpm -E %fedora)/bieszczaders-kernel-cachyos-fedora-$(rpm -E %fedora).repo -O $KERNEL_CACHYOS_REPO_FILE
  YUM_CHANGED=true
fi

if [ ! -f $KERNEL_CACHYOS_ADDONS_REPO_FILE ]
then
  wget https://copr.fedorainfracloud.org/coprs/bieszczaders/kernel-cachyos-addons/repo/fedora-$(rpm -E %fedora)/bieszczaders-kernel-cachyos-addons-fedora-$(rpm -E %fedora).repo -O $KERNEL_CACHYOS_ADDONS_REPO_FILE
  YUM_CHANGED=true
fi

if [ YUM_CHANGED == true ]
then
     dnf repoquery
fi