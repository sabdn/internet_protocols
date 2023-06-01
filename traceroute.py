import argparse
from cymruwhois import Client
import subprocess
from tabulate import tabulate
import re
from typing import NoReturn, List, Optional, Tuple


IP_PATTERN = re.compile(r'(\d+\.\d+\.\d+\.\d+)')


class Traceroute:
    def __init__(self):
        self.client = Client()

    def run(self) -> NoReturn:
        server = self.parse_args()
        ips = self.get_ip_list(server)
        print(tabulate([[ip, *self.get_ip_info(ip)] for ip in ips],
                       headers=['IP', 'ASN', 'Owner', 'Country'],
                       tablefmt='grid'))

    def get_ip_list(self, server: str) -> List[str]:
        ips = []
        sub = subprocess.run(['tracert', '-d', server], stdout=subprocess.PIPE)
        for line in sub.stdout.decode('cp1251').split('\n')[1:]:


            ip = self.extract_ip(line)
            if ip:
                ips.append(ip)
        return ips

    def get_ip_info(self, ip: str) -> Tuple[int, str, str]:
        r = self.client.lookup(ip)
        return r.asn, r.owner, r.cc

    @staticmethod
    def extract_ip(line: str) -> Optional[str]:
        s = re.search(IP_PATTERN, line)
        return s.group(0) if s else None

    @staticmethod
    def parse_args() -> str:
        parser = argparse.ArgumentParser()
        parser.add_argument('server', type=str, help='Destination URL/IP')
        args = parser.parse_args()
        return args.server


if __name__ == '__main__':
    Traceroute().run()

