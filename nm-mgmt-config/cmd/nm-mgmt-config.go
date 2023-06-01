package main

	
import (
	"fmt"
	"os"
	"net/http"
	"io/ioutil"
	"golang.org/x/sys/unix"
	"path/filepath"
)

var netrics_v1_config = "https://netrics-config1.s3.amazonaws.com/%s/nm-exp-active-netrics.toml"
var netrics_v1_etcpath = "/etc/nm-exp-active-netrics/"
var devid = ""


func writable(path string) bool {
	return unix.Access(path, unix.W_OK) == nil
}


func main() {
	fmt.Println("/*** nm-mgmt-config 0.1 by Guilherme Martins ***/")
	fmt.Println("INFO: Checking for ENV ID variable.")
        devid = os.Getenv("BALENA_DEVICE_UUID")
        if len(devid) > 0 {
		fmt.Printf("INFO: My ID:%s\n", devid)

   		response, error := http.Get(fmt.Sprintf(netrics_v1_config, devid))
		if error != nil {
      			fmt.Printf("ERROR: get (%s)", error)
			os.Exit(1)
   		}

		body, error := ioutil.ReadAll(response.Body)
   		if error != nil {
      			fmt.Printf("ERROR: ioread (%s)", error)
			os.Exit(1)
   		}
   		response.Body.Close()

		if writable(netrics_v1_etcpath) {
			error := os.WriteFile(
				filepath.Join(netrics_v1_etcpath,
					      "nm-exp-active-netrics.toml",
					     ), body, 0755)
			if error != nil {
                        	fmt.Printf("ERROR: write config (%s)", error)
                        	os.Exit(1)
			}
		} else {
			fmt.Printf("ERROR: path %s not writable", netrics_v1_etcpath)
			os.Exit(1)
                }

        } else {
		fmt.Println("ERROR: env BALENA_DEVICE_UUID not set or invalid. Exiting...")
		os.Exit(1)
        }
}
