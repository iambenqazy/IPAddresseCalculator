# Calculate Classfull Addresses
import sys
from typing import List, Tuple


class IPOctet:

    def __init__(self, ip_address, subnet_mask=24):
        self.ip_address = ip_address
        self.subnet_mask = subnet_mask
        self.octet_range = list(range(0, 256))
        self.TOTAL_SUBNET_BIT = 32
        self.bintodec_list = (128, 64, 32, 16, 8, 4, 2, 1)

    def validate_ip_address(self) -> List[int]:
        """
        Validate octet. an octet should be numbers separated by dots
        :return a list and a boolean
        """
        ip_list = self.ip_address.split('.')  # split ip address into a list

        for address in ip_list:
            if (address.isnumeric() and int(address) in self.octet_range) and len(ip_list) == 4:
                continue
            else:
                raise ValueError("Invalid IP Address.")

        validated_ip_address = [int(number) for number in ip_list]
        return validated_ip_address

    def network_bits_needed(self, number=20):
        """
        Steps Based on Networks needed
        1. Convert the number of networks that you need to binary <NB: It’s always best to subtract one from the
        number of networks needed before calculating the number of bits: eg. 5 networks; 5 - 1 = 4>
        """
        if number <= 1:
            return 0
        network_bits_needed = len(bin(number - 1)[2:])
        return network_bits_needed

    def ip_class_name(self):
        """
        Check the first octet of the ip address and return the class type
        :return: Class name as string
        """
        address = self.validate_ip_address()[0]
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

    def network_increment_number(self):
        increment_position = (self.subnet_mask + self.network_bits_needed()) % 8
        increment_number = self.bintodec_list[increment_position - 1]
        return increment_number

    def network_id(self, if_range=True):
        """
        Calculate and return a list of all network ids
        :return: a list
        """
        if self.network_bits_needed() == 0:
            return 0

        range_list = [0]
        range_increment = self.network_increment_number()
        networks_needed = 2 ** self.network_bits_needed()

        for ip_number in range(0, networks_needed):
            range_list.append(range_list[ip_number] + range_increment)

        if if_range:
            return range_list
        else:
            return networks_needed

    def broadcast_id(self):
        """
        Return the last number in the ip address list
        :return: integer
        """
        if self.network_bits_needed() == 0:
            return 255
        network_range = self.network_id()[1:]
        broadcast_range = [ip_number - 1 for ip_number in network_range]

        return broadcast_range

    def host_id(self):
        """
        This calculate the total host number based on the input bit
        :return: list
        """
        # host_bit = self.TOTAL_SUBNET_BIT - (self.subnet_mask + self.network_bits_needed())
        # host_number = (2 ** host_bit) - 2

        network_ips = self.network_map_ip()

        host_ip = []
        for network in range(1, len(network_ips) + 1):
            host_ip.append(list(network_ips.get(network, ())))

        for host_list in host_ip:
            for number in range(len(host_list)):
                if number == 0:
                    host_list[number] += 1
                elif number == 1:
                    host_list[number] -= 1

        return host_ip

    def join_ip_address(self):
        """
        This returns the ip address in a dotted separated format
        :return a string of the dotted ip address
        """
        ip_address = self.validate_ip_address()
        ip_list = '.'.join(map(str, ip_address[:3]))
        return ip_list

    def network_map_ip(self):
        if self.network_bits_needed() == 0:
            return {1: (0, 255)}
        network = self.network_id()[:-1]
        broadcast = self.broadcast_id()
        network_number = list(range(1, self.network_id(False) + 1))
        network_broadcast = zip(network, broadcast)
        network_ip_number = zip(network_number, network_broadcast)

        return dict(network_ip_number)


if __name__ == '__main__':
    ip = IPOctet('192.158.45.8')
    host_ip_range = ip.host_id()
    len_of_host = len(range(host_ip_range[0][0], host_ip_range[0][1])) + 1
    network_range = ip.network_id()[:-1]
    len_of_network = len(network_range)
    print(host_ip_range)
    if isinstance(ip.network_id(), int):
        print(ip.network_id())
    else:
        print(network_range)
    print(ip.broadcast_id())
    print(f"This is a {ip.ip_class_name()} address and there are {len_of_network} networks with {len_of_host} "
          f"valid host ip addresses per network.")
    #
    # for index in range(0, len(ip.network_id())):
    #     print(f"Network {index + 1}: ")
    #     print(f"The network address is {ip.join_ip_address()}.{ip.network_id()[index]}")
    #     print(f"The First Valid address is {ip.host_id()[index]}")
    #     print(f"The Last Valid address is {ip.host_id()[index]}")
    #     # print(f"The broadcast address is {ip.join_ip_address()}.{ip.broadcast_id()[index]}")
    # for num in ip.network_map_ip():
    #     print(num)
