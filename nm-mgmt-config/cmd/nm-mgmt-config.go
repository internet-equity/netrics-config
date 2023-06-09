package main

import (
	"fmt"
	"os"
	"net/http"
	"io/ioutil"
	"golang.org/x/sys/unix"
	"path/filepath"
	"github.com/BurntSushi/toml"
)

const version = "0.1.1"

var netrics_v1_config = "https://netrics-config1.s3.amazonaws.com/%s/nm-exp-active-netrics.toml"
var netrics_v1_etcpath = "/etc/nm-exp-active-netrics/"
//var netrics_v1_etccron = "/etc/cron.d/"
var netrics_v1_etccron = "/etc/nm-exp-active-netrics/"
var devid = ""

func writable(path string) bool {
	return unix.Access(path, unix.W_OK) == nil
}

func extract_crond(conf_output string, netrics_v1_etccron string) {
	var etccrond_output = filepath.Join(netrics_v1_etccron,
                                            "cron-nm-exp-active-netrics")
        var Conf map[string]any
	data, err := os.ReadFile(conf_output)
	if err != nil {
		fmt.Printf("ERROR: reading (%s).", conf_output)
		os.Exit(1)
	}
	err=toml.Unmarshal(data, &Conf)
        for k, v := range Conf {
		if k == "cron" {
			data := v.(map[string]interface{})
                        error := os.WriteFile(etccrond_output, []byte(data["netrics"].(string)), 0644)
                        if error != nil {
                                fmt.Printf("ERROR: write config (%s)", error)
                                os.Exit(1)
                        }
		}
        }
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
			var conf_output = filepath.Join(netrics_v1_etcpath,
                                              "nm-exp-active-netrics.toml")
			error := os.WriteFile(conf_output, body, 0644)
			if error != nil {
				fmt.Printf("ERROR: write config (%s)", error)
				os.Exit(1)
			}
			extract_crond(conf_output, netrics_v1_etccron)
		} else {
			fmt.Printf("ERROR: path %s not writable", netrics_v1_etcpath)
			os.Exit(1)
                }

        } else {
		fmt.Println("ERROR: env BALENA_DEVICE_UUID not set or invalid. Exiting...")
		os.Exit(1)
        }
}
