#!/bin/bash

if [[ $EUID -eq 0 ]]; then
   echo "ERROR: This script must be run as NON-root" 
   exit 1
fi
PROC_U=$(uname -p)
PROC=arm64
mv *.deb backup/

#only check collectd version
version_go=$(cat ../cmd/nm-mgmt-config.go | grep "const version" | grep -Po '(\d)+.(\d)+.(\d)+')
version_deb=$(cat nm-mgmt-config/DEBIAN/control| grep "Version:" | grep -Po '(\d)+.(\d)+.(\d)+')

echo "golang version:" ${version_go}
echo "debian version:" ${version_deb}

if [ "${version_go}" != "${version_deb}" ];then
        echo "ERROR: python and debian version do not match."
        exit 1
fi

if [ ! -d nm-mgmt-config/usr/local/bin/ ];then
	echo "ERROR: /usr/local/bin/ not found. This dir should exist and contain nm-mgmt-config.sh"
	exit 1
fi

cp ../cmd/nm-mgmt-config ./nm-mgmt-config/usr/local/bin/

fakeroot dpkg-deb --build nm-mgmt-config

mv nm-mgmt-config.deb nm-mgmt-config-v${version_go}-${PROC}.deb
cp nm-mgmt-config-v${version_go}-${PROC}.deb ~/nm-mgmt-config-v${version_go}-${PROC}.deb
