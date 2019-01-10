package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"regexp"
	"time"

	"github.com/google/gopacket"
	"github.com/google/gopacket/layers"
	"github.com/google/gopacket/pcap"
)

const (
	tftpdir = "/var/lib/tftpboot"
)

type dhcpID struct {
	ClientID string
	ClassID  string
}

func main() {
	var (
		device                    = "eth1"
		snapshotLen int32         = 1024
		promiscuous               = false
		timeout     time.Duration = 30 * time.Second
	)

	inDHCP := make(chan interface{})

	// Create a live packet handler on eth1
	handle, err := pcap.OpenLive(device, snapshotLen, promiscuous, timeout)
	if err != nil {
		log.Fatal(err)
	}
	defer handle.Close()

	// filter on server bound
	// TFTP traffic
	filter := "udp and port 67"
	err = handle.SetBPFFilter(filter)
	if err != nil {
		log.Fatal(err)
	}
	// Use the handle as a packet source to process all
	// packets
	ps := gopacket.NewPacketSource(handle, handle.LinkType())
	for packet := range ps.Packets() {
		DHCPLayer := packet.Layer(layers.LayerTypeDHCPv4)

		if DHCPLayer != nil {
			dhcp, _ := DHCPLayer.(*layers.DHCPv4)
			id, is9k := parseDHCPOpts(dhcp)
			if is9k {
				err := updateConfigName(id)
				if err != nil {
					log.Fatal(err)
				}
			}
		}
	}
}

func parseDHCPOpts(dhcp *layers.DHCPv4) (id dhcpID, is9k bool) {
	for _, opt := range dhcp.Options {
		if opt.Type.String() == "ClassID" {
			if string(opt.Data) != "Cisco N9K-NXOSV" {
				return id, false
			}
		}
		if opt.Type.String() == "ClientID" {
			id.ClientID = string(opt.Data)
		}
	}
	return id, true
}

func updateConfigName(id dhcpID) error {
	fn := fmt.Sprintf("cfg.%s", id.ClientID)
	fnMD5 := fmt.Sprintf("%s.md5", fn)

	log.Printf("checking for config file named: %s\n", fn)

	_, err := os.Stat(fn)
	_, err = os.Stat(fnMD5)
	// if both files exist (config/md5),
	// all is good, return from func
	if !os.IsNotExist(err) {
		return nil
	}

	// delete existing config/md5 files
	files, err := ioutil.ReadDir(tftpdir)
	if err != nil {
		return err
	}
	for _, file := range files {
		if match, err := regexp.Match(`conf.\d{11}.*`, file.Name()); err != nil {
			return err
		}
		if match {
			fmt.Println(file.Name())
		}
	}
	// write new files

	return nil
}
