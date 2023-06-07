
all:
	echo "RUN: export GOPATH=${PWD}"
	go get github.com/BurntSushi/toml
	go get golang.org/x/sys/unix
	go build -o cmd/nm-mgmt-config cmd/nm-mgmt-config.go
	cd deb; ./build.sh 
