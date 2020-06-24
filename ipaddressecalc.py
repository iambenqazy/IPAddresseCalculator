# Calculate Classfull Addresses
import sys
from typing import List, Tuple


class IPOctet:

    def __init__(self, ip_address, subnet_mask=24):
        self.ip_address = ip_address
        self.subnet_mask = subnet_mask
        self.octet_range = list(range(0, 256))
        self.TOTAL_SUBNET_BIT = 32

        ip_list, verified = self.validate_ip_address()
        if not verified:
            raise ValueError("Invalid IP Address.")

    def validate_ip_address(self) -> Tuple[List[int], bool]:
        """
        Validate octet. an octet should be numbers separated by dots

        """
        ip_list = self.ip_address.split('.')  # split ip address into a list

        for address in ip_list:
            try:
                address_range = int(address) in self.octet_range
            except ValueError:
                return [], False
            if not address_range:
                return [], False

        return ip_list, True

    def ip_class_name(self):
        """
        Check the first octet of the ip address and return the class type
        :return: Class name as string
        """
        address = int(self.validate_ip_address()[0][0])
        if address in self.octet_range[:128]:
            return "Class A"
        elif address in self.octet_range[128:192]:
            return "Class B"
        elif address in self.octet_range[192:224]:
            return "Class C"
        elif address in self.octet_range[224:240]:
            return "Class D"
        elif address in self.octet_range[240:]:
            return "Class E"

    def netmask_id(self):
        pass

    def host_id(self, use_valid=True):
        """
        This calculate the total host number based on the input bit
        :param use_valid: bool
        :return: generator
        """
        host_number = 2 ** (self.TOTAL_SUBNET_BIT - self.subnet_mask)
        total_host_ip = list(range(0, host_number))
        valid_ip_address = total_host_ip[1:-1]

        if use_valid:
            for number in valid_ip_address:
                yield number
        else:
            for number in total_host_ip:
                yield number

    def network_id(self):
        """
        Return the first number in the ip address list
        :return: integer
        """
        network_ip = list(self.host_id(False))[0]
        return network_ip

    def broadcast_id(self):
        """
        Return the last number in the ip address list
        :return: integer
        """
        broadcast_ip = list(self.host_id(False))[-1]
        return broadcast_ip

    def join_ip_address(self):
        """
        This returns the ip address in a dotted separated format
        :return a string of the dotted ip address
        """
        ip_address = self.validate_ip_address()[0]
        ip_list = '.'.join(map(str,ip_address[:3]))
        return ip_list


def networks_needed(number):
    """
    Steps Based on Networks needed 1. Convert the number of networks that you need to binary <NB: It’s always best to
    subtract one from the number of networks needed before calculating the number of bits: eg. 5 networks; 5 - 1 = 4>
    2. Reserve bits in the mask and find your increment 3. Use increment to generate networks ranges
    """
    pass


if __name__ == '__main__':
    ip = IPOctet('174.158.45.23')
    host_ip_range = [number for number in ip.host_id()]

    print(f"This is a {ip.ip_class_name()} address and there are {len(host_ip_range)} "
          f"valid host ip addresses starting from {ip.join_ip_address()}.{host_ip_range[0]} to "
          f"{ip.join_ip_address()}.{host_ip_range[-1]}")
    print(f"The network id is {ip.join_ip_address()}.{ip.network_id()}")
    print(f"The broadcast id is {ip.join_ip_address()}.{ip.broadcast_id()}")
