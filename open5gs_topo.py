#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""
About: Basic example of using Docker as a Mininet host.
       Like upstream Mininet, the network topology can be either created by
       provide a topology class or directly using the network object.

Topo: Two Docker hosts (h1, h2) connected directly to a single switch (s1).

Tests:
- Iperf UDP bandwidth test between h1 and h2.
- Packet losses test with ping and increased link loss rate.
"""

import comnetsemu.tool as tool
from comnetsemu.net import Containernet
from comnetsemu.node import DockerHost
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller, OVSBridge
from mininet.topo import Topo
from mininet.cli import CLI

import os
from dotenv import dotenv_values, load_dotenv

PING_COUNT = 15
load_dotenv()

def run_net():

    setLogLevel("info")

    # To be tested parameters at runtime
    loss_rates = [30]

    env = dict(dotenv_values(".env"))

    net = Containernet(controller=Controller, link=TCLink)

    info("*** Adding controller\n")
    net.addController("c0")

    info("*** Adding switch\n")
    s1 = net.addSwitch("s1")

    info("*** Adding hosts\n")
    env["COMPONENT_NAME"]="ausf-1"
    ausf = net.addDockerHost(
        "ausf",
        dimage="docker_open5gs",
        dcmd="/open5gs_init.sh",
        ip=os.environ["AUSF_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/ausf:/mnt/ausf:rw",
                "/home/vagrant/docker_open5gs/log:/open5gs/install/var/log/open5gs:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ]
        },
    )
    net.addLink(ausf, s1, bw=1000, delay="1ms", intfName1="ausf-s1", intfName2="s1-ausf")

    mongo = net.addDockerHost(
        "mongo",
        dimage="docker_mongo",
        dcmd="/mnt/mongo/mongo_init.sh",
        ip=os.environ["MONGO_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/mongo:/mnt/mongo:rw",
                "/home/vagrant/docker_open5gs/mongodbdata:/var/lib/mongodb:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ]
        },
    )
    net.addLink(mongo, s1, bw=1000, delay="1ms", intfName1="mongo-s1", intfName2="s1-mongo")

    env["COMPONENT_NAME"]="webui"
    webui = net.addDockerHost(
        "webui",
        dimage="docker_open5gs",
        dcmd="/open5gs_init.sh",
        ip=os.environ["WEBUI_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/webui:/mnt/webui:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ],
            "ports" : { "3000/tcp": 3000 }
        },
    )
    net.addLink(webui, s1, bw=1000, delay="1ms", intfName1="webui-s1", intfName2="s1-webui")

    env["COMPONENT_NAME"]="nrf-1"
    nrf = net.addDockerHost(
        "nrf",
        dimage="docker_open5gs",
        dcmd="/open5gs_init.sh",
        ip=os.environ["NRF_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/nrf:/mnt/nrf:rw",
                "/home/vagrant/docker_open5gs/log:/open5gs/install/var/log/open5gs:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ]
        },
    )
    net.addLink(nrf, s1, bw=1000, delay="1ms", intfName1="nrf-s1", intfName2="s1-nrf")

    env["COMPONENT_NAME"]="udr-1"
    udr = net.addDockerHost(
        "udr",
        dimage="docker_open5gs",
        dcmd="/open5gs_init.sh",
        ip=os.environ["UDR_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/udr:/mnt/udr:rw",
                "/home/vagrant/docker_open5gs/log:/open5gs/install/var/log/open5gs:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ]
        },
    )
    net.addLink(udr, s1, bw=1000, delay="1ms", intfName1="udr-s1", intfName2="s1-udr")

    env["COMPONENT_NAME"]="udm-1"
    udm = net.addDockerHost(
        "udm",
        dimage="docker_open5gs",
        dcmd="/open5gs_init.sh",
        ip=os.environ["UDM_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/udm:/mnt/udm:rw",
                "/home/vagrant/docker_open5gs/log:/open5gs/install/var/log/open5gs:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ]
        },
    )
    net.addLink(udm, s1, bw=1000, delay="1ms", intfName1="udm-s1", intfName2="s1-udm")
    
    env["COMPONENT_NAME"]="pcf-1"
    pcf = net.addDockerHost(
        "pcf",
        dimage="docker_open5gs",
        dcmd="/open5gs_init.sh",
        ip=os.environ["PCF_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/pcf:/mnt/pcf:rw",
                "/home/vagrant/docker_open5gs/log:/open5gs/install/var/log/open5gs:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ]
        },
    )
    net.addLink(pcf, s1, bw=1000, delay="1ms", intfName1="pcf-s1", intfName2="s1-pcf")

    env["COMPONENT_NAME"]="bsf-1"
    bsf = net.addDockerHost(
        "bsf",
        dimage="docker_open5gs",
        dcmd="/open5gs_init.sh",
        ip=os.environ["BSF_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/bsf:/mnt/bsf:rw",
                "/home/vagrant/docker_open5gs/log:/open5gs/install/var/log/open5gs:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ]
        },
    )
    net.addLink(bsf, s1, bw=1000, delay="1ms", intfName1="bsf-s1", intfName2="s1-bsf")

    env["COMPONENT_NAME"]="nssf-1"
    nssf = net.addDockerHost(
        "nssf",
        dimage="docker_open5gs",
        dcmd="/open5gs_init.sh",
        ip=os.environ["NSSF_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/nssf:/mnt/nssf:rw",
                "/home/vagrant/docker_open5gs/log:/open5gs/install/var/log/open5gs:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ]
        },
    )
    net.addLink(nssf, s1, bw=1000, delay="1ms", intfName1="nssf-s1", intfName2="s1-nssf")

    env["COMPONENT_NAME"]="smf-1"
    smf = net.addDockerHost(
        "smf",
        dimage="docker_open5gs",
        dcmd="/open5gs_init.sh",
        ip=os.environ["SMF_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/smf:/mnt/smf:rw",
                "/home/vagrant/docker_open5gs/log:/open5gs/install/var/log/open5gs:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ]
        },
    )
    net.addLink(smf, s1, bw=1000, delay="1ms", intfName1="smf-s1", intfName2="s1-smf")

    env["COMPONENT_NAME"]="upf-1"
    upf = net.addDockerHost(
        "upf",
        dimage="docker_open5gs",
        dcmd="/open5gs_init.sh",
        ip=os.environ["UPF_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/upf:/mnt/upf:rw",
                "/home/vagrant/docker_open5gs/log:/open5gs/install/var/log/open5gs:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ],
            "cap_add": "NET_ADMIN",
            "sysctls": {"net.ipv4.ip_forward": 1},
            "devices": "/dev/net/tun:/dev/net/tun:rwm"
        },
    )
    net.addLink(upf, s1, bw=1000, delay="1ms", intfName1="upf-s1", intfName2="s1-upf")

    env["COMPONENT_NAME"]="hss-1"
    hss = net.addDockerHost(
        "hss",
        dimage="docker_open5gs",
        dcmd="/open5gs_init.sh",
        ip=os.environ["HSS_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/hss:/mnt/hss:rw",
                "/home/vagrant/docker_open5gs/log:/open5gs/install/var/log/open5gs:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ]
        },
    )
    net.addLink(hss, s1, bw=1000, delay="1ms", intfName1="hss-s1", intfName2="s1-hss")

    env["COMPONENT_NAME"]="sgwc-1"
    sgwc = net.addDockerHost(
        "sgwc",
        dimage="docker_open5gs",
        dcmd="/open5gs_init.sh",
        ip=os.environ["SGWC_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/sgwc:/mnt/sgwc:rw",
                "/home/vagrant/docker_open5gs/log:/open5gs/install/var/log/open5gs:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ]
        },
    )
    net.addLink(sgwc, s1, bw=1000, delay="1ms", intfName1="sgwc-s1", intfName2="s1-sgwc")

    env["COMPONENT_NAME"]="sgwu-1"
    sgwu = net.addDockerHost(
        "sgwu",
        dimage="docker_open5gs",
        dcmd="/open5gs_init.sh",
        ip=os.environ["SGWU_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/sgwu:/mnt/sgwu:rw",
                "/home/vagrant/docker_open5gs/log:/open5gs/install/var/log/open5gs:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ]
        },
    )
    net.addLink(sgwu, s1, bw=1000, delay="1ms", intfName1="sgwu-s1", intfName2="s1-sgwu")

    env["COMPONENT_NAME"]="amf-1"
    amf = net.addDockerHost(
        "amf",
        dimage="docker_open5gs",
        dcmd="/open5gs_init.sh",
        ip=os.environ["AMF_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/amf:/mnt/amf:rw",
                "/home/vagrant/docker_open5gs/log:/open5gs/install/var/log/open5gs:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ]
        },
    )
    net.addLink(amf, s1, bw=1000, delay="1ms", intfName1="amf-s1", intfName2="s1-amf")

    env["COMPONENT_NAME"]="mme-1"
    mme = net.addDockerHost(
        "mme",
        dimage="docker_open5gs",
        dcmd="/open5gs_init.sh",
        ip=os.environ["MME_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/mme:/mnt/mme:rw",
                "/home/vagrant/docker_open5gs/log:/open5gs/install/var/log/open5gs:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ]
        },
    )
    net.addLink(mme, s1, bw=1000, delay="1ms", intfName1="mme-s1", intfName2="s1-mme")

    env["COMPONENT_NAME"]="pcrf-1"
    pcrf = net.addDockerHost(
        "pcrf",
        dimage="docker_open5gs",
        dcmd="/open5gs_init.sh",
        ip=os.environ["PCRF_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/pcrf:/mnt/pcrf:rw",
                "/home/vagrant/docker_open5gs/log:/open5gs/install/var/log/open5gs:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ]
        },
    )
    net.addLink(pcrf, s1, bw=1000, delay="1ms", intfName1="pcrf-s1", intfName2="s1-pcrf")

    dns = net.addDockerHost(
        "dns",
        dimage="docker_dns",
        dcmd="/mnt/dns/dns_init.sh",
        ip=os.environ["DNS_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/dns:/mnt/dns:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ]
        },
    )
    net.addLink(dns, s1, bw=1000, delay="1ms", intfName1="dns-s1", intfName2="s1-dns")

    env["TABLE"]="0"
    env["INTERFACE"]=os.environ["RTPENGINE_IP"]
    env["LISTEN_NG"]=os.environ["RTPENGINE_IP"] + "2223"
    env["PIDFILE"]="/run/ngcp-rtpengine-daemon.pid"
    env["PORT_MAX"]="50000"
    env["PORT_MIN"]="49000"
    env["NO_FALLBACK"]="no"
    env["TOS"]="184"
    rtpengine = net.addDockerHost(
        "rtpengine",
        dimage="docker_rtpengine",
        dcmd="/mnt/rtpengine/rtpengine_init.sh",
        ip=os.environ["RTPENGINE_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/rtpengine:/mnt/rtpengine:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ],
            "cap_add": "NET_ADMIN"
        },
    )
    net.addLink(rtpengine, s1, bw=1000, delay="1ms", intfName1="rtpengine-s1", intfName2="s1-rtpengine")

    env = dict(dotenv_values(".env"))
    mysql = net.addDockerHost(
        "mysql",
        dimage="docker_mysql",
        dcmd="/mysql_init.sh",
        ip=os.environ["MYSQL_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ]
        },
    )
    net.addLink(mysql, s1, bw=1000, delay="1ms", intfName1="mysql-s1", intfName2="s1-mysql")

    env["COMPONENT_NAME"]="fhoss-1"
    fhoss = net.addDockerHost(
        "fhoss",
        dimage="docker_fhoss",
        dcmd="/mnt/fhoss/fhoss_init.sh",
        ip=os.environ["FHOSS_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/fhoss:/mnt/fhoss:rw",
                "/home/vagrant/docker_open5gs/log:/open5gs/install/var/log/open5gs:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ],
            "dns": [os.environ["DNS_IP"]]
        },
    )
    net.addLink(fhoss, s1, bw=1000, delay="1ms", intfName1="fhoss-s1", intfName2="s1-fhoss")

    env["COMPONENT_NAME"]="icscf-1"
    icscf = net.addDockerHost(
        "icscf",
        dimage="docker_kamailio",
        dcmd="/kamailio_init.sh",
        ip=os.environ["ICSCF_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/icscf:/mnt/icscf:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ],
            "dns": [os.environ["DNS_IP"]]
        },
    )
    net.addLink(icscf, s1, bw=1000, delay="1ms", intfName1="icscf-s1", intfName2="s1-icscf")

    env["COMPONENT_NAME"]="scscf-1"
    scscf = net.addDockerHost(
        "scscf",
        dimage="docker_kamailio",
        dcmd="/kamailio_init.sh",
        ip=os.environ["SCSCF_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/scscf:/mnt/scscf:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ],
            "dns": [os.environ["DNS_IP"]]
        },
    )
    net.addLink(scscf, s1, bw=1000, delay="1ms", intfName1="scscf-s1", intfName2="s1-scscf")

    env["COMPONENT_NAME"]="pcscf-1"
    pcscf = net.addDockerHost(
        "pcscf",
        dimage="docker_kamailio",
        dcmd="/kamailio_init.sh",
        ip=os.environ["PCSCF_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/pcscf:/mnt/pcscf:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ],
            "dns": [os.environ["DNS_IP"]],
            "cap_add": "NET_ADMIN"
        },
    )
    net.addLink(pcscf, s1, bw=1000, delay="1ms", intfName1="pcscf-s1", intfName2="s1-pcscf")

    env["COMPONENT_NAME"]="ueransim-gnb-1"
    nr_gnb = net.addDockerHost(
        "nr_gnb",
        dimage="docker_ueransim",
        dcmd="/ueransim_image_init.sh",
        ip=os.environ["NR_GNB_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/ueransim:/mnt/ueransim:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ],
            "cap_add": "NET_ADMIN",
            "devices": "/dev/net/tun:/dev/net/tun:rwm"
        },
    )
    net.addLink(nr_gnb, s1, bw=1000, delay="1ms", intfName1="nr_gnb-s1", intfName2="s1-nr_gnb")

    env["COMPONENT_NAME"]="ueransim-ue-1"
    nr_ue = net.addDockerHost(
        "nr_ue",
        dimage="docker_ueransim",
        dcmd="/ueransim_image_init.sh",
        ip=os.environ["NR_UE_IP"] + "/24",
        docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8),
            "environment": env,
            "volumes": [
                "/home/vagrant/docker_open5gs/ueransim:/mnt/ueransim:rw",
                "/etc/timezone:/etc/timezone:ro",
                "/etc/localtime:/etc/localtime:ro"
            ],
            "cap_add": "NET_ADMIN",
            "devices": "/dev/net/tun:/dev/net/tun:rwm"
        },
    )
    net.addLink(nr_ue, s1, bw=1000, delay="1ms", intfName1="nr_ue-s1", intfName2="s1-nr_ue")





    info("*** Starting network\n")
    net.start()

    #net.pingAll()

    CLI(net)

    info("*** Stopping network")
    net.stop()

    #print(os.environ["AUSF_IP"] + "/24")
    #print(env)


class TestTopo(Topo):
    def build(self, n):
        switch = self.addSwitch("s1")
        for h in range(1, n + 1):
            host = self.addHost(
                "h%s" % h,
                cls=DockerHost,
                dimage="dev_test",
                docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8)},
            )
            self.addLink(switch, host, bw=1000, delay="1ms")


def run_topo():
    net = Containernet(
        controller=Controller, link=TCLink, switch=OVSBridge, topo=TestTopo(2)
    )

    info("*** Adding controller\n")
    net.addController("c0")

    info("*** Starting network\n")
    net.start()
    net.pingAll()
    h1 = net.get("h1")
    h2 = net.get("h2")
    net.iperf((h1, h2), l4Type="UDP", udpBw="10M")
    info("*** Stopping network")
    net.stop()


if __name__ == "__main__":
    setLogLevel("debug")
    run_net()
    #run_topo()
{"mode":"full","isActive":False}