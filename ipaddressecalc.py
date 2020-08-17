# Calculate Classfull Addresses
import sys
from typing import List, Tuple


class IPOctet:

    def __init__(self, ip_address, subnet_mask):
        self.ip_address = ip_address
        self.subnet_mask = subnet_mask
        self.OCTET_MAX_VALUE = 255
        self.OCTET_MIN_VALUE = 0
        self.TOTAL_SUBNET_BIT = 32
        self.bintodec_list = (128, 64, 32, 16, 8, 4, 2, 1)

    def check_octet_range(self, number):
        """
        This checks and return a boolean value if an address is between 0 and 255
        :param number:
        :return: bool
        """
        return self.OCTET_MIN_VALUE <= int(number) <= self.OCTET_MAX_VALUE

    def split_address(self, input_address) -> List[int]:
        """
        Validate octet. an octet should be numbers separated by dots
        :return a list and a boolean
        """
        address_value = input_address.split('.')
        for address in address_value:
            if (address.isnumeric() and self.check_octet_range(address)) and (len(address_value) == 4):
                continue
            else:
                raise ValueError("Invalid Address Number.")

        validated_ip_address = [int(number) for number in address_value]
        return validated_ip_address

    def validate_ip_address(self):
        """
        This returns the validated form of the input ip address
        :return: list
        """
        return self.split_address(self.ip_address)

    def validate_subnetmask(self):
        """
        This returns the validated form of the input subnetmask number
        :return: int if cidr notation(/24 -> 24) or list if decimal notation(255.255.255.0 -> [255],[255],[255],[0])
        """
        input_subnetmask = self.subnet_mask
        input_subnetmask_length = len(input_subnetmask)

        if (input_subnetmask_length == 3) and (input_subnetmask.startswith('/')):
            if (input_subnetmask[1:].isnumeric()) and (int(input_subnetmask[1:]) <= self.TOTAL_SUBNET_BIT):
                cidr_subnetmask = int(input_subnetmask[1:])
                return cidr_subnetmask
        elif 6 < input_subnetmask_length < 16:
            return self.split_address(input_subnetmask)  # validate and return a list of the address
        else:
            raise ValueError("Invalid CIDR Number.")

    def network_bits_needed(self, number=5):
        """
        Steps Based on Networks needed
        1. Convert the number of networks that you need to binary <NB: It’s always bes®t to subtract one from the
        number of networks needed before calculating the number of bits: eg. 5 networks; 5 - 1 = 4>
        """
        if number <= 1:
            return 0
        input_bit = len(bin(number - 1)[2:])
        remaining_bit = self.TOTAL_SUBNET_BIT - self.validate_subnetmask()
        host_bit = remaining_bit - input_bit
        if host_bit <= 1:
            raise ValueError("Invalid Network Number")
        return input_bit

    def subnet_number_needed(self):
        """
        This calculates the new subnet mask based on the input subnet mask of the ip address
        :return: integer
        """
        network_bits_needed = self.network_bits_needed()
        subnet_number = self.validate_subnetmask() + network_bits_needed
        if subnet_number > 30 or subnet_number < 0:
            raise ValueError("Invalid Subnet Number")
        return subnet_number

    def ip_class_name(self):
        """
        Check the first octet of the ip address and return the class type
        :return: Class name as string
        """
        octet_range = list(range(self.OCTET_MIN_VALUE, (self.OCTET_MAX_VALUE + 1)))
        address = self.validate_ip_address()[0]
        if address in octet_range[:128]:
            return "Class A"
        elif address in octet_range[128:192]:
            return "Class B"
        elif address in octet_range[192:224]:
            return "Class C"
        elif address in octet_range[224:240]:
            return "Class D"
        elif address in octet_range[240:]:
            return "Class E"

    def subnetmask_cidr_conversion(self):
        """
        This convert subnetmask id from cidr to decimal notation and vice versa
        :return:
        """
        pass

    def network_increment_number(self):
        increment_position = (self.validate_subnetmask() + self.network_bits_needed()) % 8
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
        network_id_range = self.network_id()[1:]
        broadcast_id_range = [ip_number - 1 for ip_number in network_id_range]

        return broadcast_id_range

    def host_id(self):
        """
        Calculates the valid host range per network
        :return: list
        """
        # host_bit = self.TOTAL_SUBNET_BIT - (self.subnet_mask + self.network_bits_needed())
        # host_number = (2 ** host_bit) - 2

        network_ips = self.network_map_ip()

        host_ip = []
        for network in range(1, len(network_ips) + 1):
            host_ip.append(list(network_ips.get(network, ())))  # this returns a list of values in the dictionary

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
        """
        Create a dictionary of network_id map to broadcast_id for each network.

        :return: a dictionary
        """
        if self.network_bits_needed() == 0:
            return {1: (0, 255)}
        network = self.network_id()[:-1]
        broadcast = self.broadcast_id()
        network_number = list(range(1, self.network_id(False) + 1))
        network_broadcast = zip(network, broadcast)
        network_ip_number = zip(network_number, network_broadcast)

        return dict(network_ip_number)


if __name__ == '__main__':
    ip = IPOctet('192.168.8.8', '/27')
    host_ip_range = ip.host_id()
    len_of_host = len(range(host_ip_range[0][0], host_ip_range[0][1])) + 1
    if isinstance(ip.network_id(), int) and isinstance(ip.broadcast_id(), int):
        network_range = [ip.network_id()]
        broadcast_range = [ip.broadcast_id()]
    else:
        network_range = ip.network_id()[:-1]
        broadcast_range = ip.broadcast_id()
    len_of_network = len(network_range)
    network_map = list(zip(network_range, broadcast_range))
    print(f"Host IP range: {host_ip_range}")
    print(f"Network and Broadcast ID range: {network_map}")

    print(f"This is a {ip.ip_class_name()} address and there are {len_of_network} networks with {len_of_host} "
          f"valid host ip addresses per network and a subnet mask of /{ip.subnet_number_needed()}")

    # for index in range(0, len(ip.network_id())):
    #     print(f"Network {index + 1}: ")
    #     print(f"The network address is {ip.join_ip_address()}.{ip.network_id()[index]}")
    #     print(f"The First Valid address is {ip.host_id()[index]}")
    #     print(f"The Last Valid address is {ip.host_id()[index]}")
    #     # print(f"The broadcast address is {ip.join_ip_address()}.{ip.broadcast_id()[index]}")
    # for num in ip.network_map_ip():
    #     print(num)
