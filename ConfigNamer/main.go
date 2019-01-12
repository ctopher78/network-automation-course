package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
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

	// Create a live packet handler on eth1
	handle, err := pcap.OpenLive(device, snapshotLen, promiscuous, timeout)
	if err != nil {
		log.Fatal(err)
	}
	defer handle.Close()

	// filter on server bound
	// TFTP traffic
	filter := "udp and dst port 67"
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
			// the clientID returned has
			// unprintable characters, which break
			// os.Stat().  They need to be removed
			// immediately.
			s := fmt.Sprintf("%s", opt.Data)
			re, err := regexp.Compile(`\x00`)
			if err != nil {
				log.Fatal()
			}
			clean := re.ReplaceAllLiteralString(s, "")
			id.ClientID = clean
		}
	}
	return id, true
}

func updateConfigName(id dhcpID) error {
	fn := fmt.Sprintf("conf.%s", id.ClientID)
	fnMD5 := fmt.Sprintf("%s.md5", fn)

	fpath := filepath.Join(tftpdir, fn)
	fpathMd5 := filepath.Join(tftpdir, fnMD5)

	log.Printf("checking for config file named: %s\n", fn)
	_, err := os.Stat(fpath)
	_, errmd5 := os.Stat(fpathMd5)
	fmt.Println(err)
	fmt.Println(errmd5)
	// if both files exist (config/md5),
	// all is good, return from func
	if !os.IsNotExist(err) || !os.IsNotExist(errmd5) {
		return nil
	}

	// delete existing config/md5 files
	files, err := ioutil.ReadDir(tftpdir)
	if err != nil {
		return err
	}

	cfgRE, err := regexp.Compile(`conf.\S{11}.*`)
	var match bool
	for _, file := range files {
		oldconfig := filepath.Join(tftpdir, file.Name())
		oldmd5 := filepath.Join(tftpdir, file.Name()+".md5")
		match = cfgRE.Match([]byte(file.Name()))
		if match {
			// rename old config file
			err = os.Rename(oldconfig, fpath)
			if err != nil {
				log.Print(err)
			}
			// rename md5 file
			err = os.Rename(oldmd5, fpathMd5)
			if err != nil {
				log.Print(err)
			}
		}
	}

	return nil
}
