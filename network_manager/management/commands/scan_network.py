import subprocess
import xmltodict

from datetime import datetime
from django_daemon_command.management.base import DaemonCommand

from network_manager.models import Host, Port, NmapRun, RunStat


class Command(DaemonCommand):
    sleep = 3600

    def add_arguments(self, parser):
        parser.add_argument("network", type=str)

    def process(self, *args, **options):
        self.log("Network scan completed!")

    def handle(self, *args, **options):
        if options["network"]:
            network = options["network"]
        else:
            network = "192.168.1.0/24"

        xml_file = "networkscan.xml"
        cmd = ["sudo", "nmap", "-v", "-n", "-p-", "-sT", "-sV", "-O", "--osscan-limit", "--max-os-tries", "3",
               network,  "-oX", xml_file]
        subprocess.run(cmd)
        read_scan_results_and_save_to_database(xml_file)
        self.daemonize(*args, **options)

    def on_exception(self, exc):
        self.print_exception(exc)
        self.save_exception(exc)


def get_nmap_run_details(nmap_run):
    nmap_run_values = {}
    nmap_run_detail_keys = [
        "scanner",
        "args",
        "start",
        "startstr",
        "version",
        "xmloutputversion",
        "verbose",
        "debugging"
    ]

    for key in nmap_run_detail_keys:
        value = nmap_run[key]
        if type(value) == dict:
            if "level" in value.keys():
                nmap_run_values[f"{key}_level"] = int(value["level"])
        else:
            nmap_run_values[f"{key}"] = value
    return nmap_run_values


def get_run_stats_details(nmap_run):
    runstats = nmap_run["runstats"]
    runstats_keys = ["finished", "hosts"]
    runstats_details = {}

    for key in runstats_keys:
        values = runstats[key]
        for item in values:
            if item == "timestr":
                runstats_details[f"{key}_{item}"] = datetime.strptime(values[item], "%a %b %d %H:%M:%S %Y")
            else:
                runstats_details[f"{key}_{item}"] = values[item]

    return runstats_details


def up(host):
    if host["status"]["state"] == "up":
        return True
    else:
        return False


def get_hosts_details(nmap_run):
    hosts_values = []
    try:
        hosts_list = nmap_run["host"]
        hosts = filter(up, hosts_list)
        host_details = {}
        host_keys = ["status", "address", "hostnames", "ports", "os"]
        for host in hosts:
            for key in host_keys:
                if key == "hostnames":
                    host_details["hostname"] = host[key]
                elif key == "address":
                    addresses = host[key]
                    for address in addresses:
                        if type(address) == str:
                            pass
                        else:
                            address_type = address['addrtype']
                            host_details[f"{address_type}_address"] = address["addr"]
                            if address_type == "mac":
                                try:
                                    host_details["vendor"] = address["vendor"]
                                except KeyError:
                                    host_details["vendor"] = ""
                elif key == "ports":
                    ports = host["ports"]["port"]
                    host_details["ports"] = ports
                elif key == "os":
                    if type(host["os"]["os_match"]) == list:
                        host_os_name = host["os"]["osmatch"][0]["name"]

                    else:
                        host_os_name = host["os"]["osmatch"]["name"]

                    host_details["os_name"] = host_os_name

                    if type(host["os"]["osmatch"]["osclass"]) == list:
                        os_details = host["os"]["osmatch"]["osclass"][0]
                    else:
                        os_details = host["os"]["osmatch"]["osclass"]

                    host_details["os_details"] = os_details
                else:
                    values = host[key]
                    for value in values:
                        host_details[f"{key}_{value}"] = values[value]
            hosts_values.append(host_details)
    except KeyError:
        pass
    return hosts_values


def read_scan_results_and_save_to_database(xml_file):
    with open(xml_file, mode="rb") as xml_file:
        nmap_run_dict = xmltodict.parse(xml_file.read(), attr_prefix='')

    nmap_run = nmap_run_dict["nmaprun"]
    hosts = get_hosts_details(nmap_run)
    nmap_run_details = get_nmap_run_details(nmap_run)
    runstats_details = get_run_stats_details(nmap_run)

    nmap_run = NmapRun.objects.create(**nmap_run_details)
    runstats_details["nmap_run"] = nmap_run
    RunStat.objects.create(**runstats_details)

    for host in hosts:
        new_host = Host.objects.update_or_create(mac_address=host["mac_address"],
                                                 defaults={
                                                      "ipv4_address": host["ipv4_address"],
                                                      "vendor": host["vendor"],
                                                      "hostname": host["hostname"],
                                                      "os_name": host["os_name"],
                                                      "osclass_type": host["os_details"]["type"],
                                                      "cpe": host["os_details"]["cpe"],
                                                      "status_state": host["status_state"],
                                                      "status_reason": host["status_reason"],
                                                      "status_reason_ttl": host["status_reason_ttl"]})

        for port in host["ports"]:
            if port["service"]["extrainfo"]:
                service_extra_info = port["service"]["extrainfo"]
            else:
                service_extra_info = ""
            Port.objects.update_or_create(
                host=new_host,
                port_id=port["portid"],
                defaults={
                    "protocol": port["protocol"],
                    "state": port["state"]["state"],
                    "reason": port["state"]["reason"],
                    "reason_ttl" : port["state"]["reason_ttl"],
                    "service_name": port["service"]["name"],
                    "service_product": port["service"]["product"],
                    "service_version": port["service"]["version"],
                    "service_extra_info": service_extra_info,
                    "service_method": port["service"]["method"],
                    "service_conf": port["service"]["conf"],
                    "service_cpe": port["service"]["cpe"]
                }
            )
