# Calculate Classfull Addresses
import sys
from typing import List, Tuple


class IPOctet:

    def __init__(self, ip_address, subnet_mask, networks_needed):
        self.ip_address = ip_address
        self.subnet_mask = subnet_mask
        self.networks_needed = networks_needed
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

    def check_octet_position(self, subnet_mask=None):
        """
        This checks the subnet mask bit and returns the octet position
        :param subnet_mask:
        :return: int
        """
        subnet_bit = subnet_mask or self.subnetmask_decimal_to_cidr()
        if subnet_bit != 32:
            return int(subnet_bit / 8) + 1
        else:
            return int(subnet_bit / 8)

    def split_address(self, input_address) -> List[int]:
        """
        This splits a string of input address into a list and checks if its numeric
        :return a list
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

    def validate_subnetmask(self, input_subnetmask=None):
        """
        This returns the validated form of the input subnetmask number
        :return: int if cidr notation(/24 -> 24) or list if decimal notation(255.255.255.0 -> [255],[255],[255],[0])
        """
        # this assigns the subnet_mask if the input parameter is None
        input_subnetmask_value = input_subnetmask or self.subnet_mask
        if str(input_subnetmask_value).isnumeric():
            input_subnetmask_value = "/" + str(input_subnetmask_value)

        input_subnetmask_length = len(input_subnetmask_value)
        if (input_subnetmask_length == 3) and (input_subnetmask_value.startswith('/')):
            input_cidr_bit = input_subnetmask_value.split('/')
            if (input_cidr_bit[1].isnumeric()) and (int(input_cidr_bit[1]) <= self.TOTAL_SUBNET_BIT):
                cidr_subnetmask = int(input_cidr_bit[1])
                return cidr_subnetmask
        elif 6 < input_subnetmask_length < 16:
            new_input_subnetmask = self.split_address(input_subnetmask_value)
            for octet_index, octet in enumerate(new_input_subnetmask):
                for octet_position in range(0, octet_index):
                    if octet <= new_input_subnetmask[octet_position]:
                        continue
                    else:
                        raise ValueError("Invalid Subnet Value")
            return new_input_subnetmask  # validate and return a list of the address
        else:
            raise ValueError("Invalid Subnet Number")

    def subnetmask_cidr_to_decimal(self, subnet_value=None):
        """
        This convert subnet bit value from cidr to decimal notation
        :return: list
        """
        subnet_bit = self.validate_subnetmask(subnet_value) or self.validate_subnetmask()
        bit_value = self.bintodec_list
        subnet_list = []

        if type(subnet_bit) is int:
            if not 8 <= subnet_bit <= 32:
                raise ValueError("Invalid Subnet Address")
            for octet in range(0, 4):
                if not subnet_bit < 8:
                    subnet_list.insert(octet, sum(bit_value))
                    subnet_bit -= 8
                elif not subnet_bit == 0:
                    subnet_list.insert(octet, sum(bit_value[:subnet_bit]))
                    subnet_bit -= subnet_bit
                else:
                    subnet_list.insert(octet, subnet_bit)

            if len(subnet_list) == 4:
                return subnet_list
            else:
                return []

    def subnetmask_decimal_to_cidr(self, subnet_mask=None):
        """
        This converts decimal notation to cidr of the subnetmask
        :param : list
        :return: int for the bit value
        """
        subnet_id = subnet_mask or self.validate_subnetmask()
        cidr_bit = 0
        if type(subnet_id) is list:
            for address in subnet_id:
                cidr_bit += bin(address).count('1')
            return cidr_bit
        else:
            return subnet_id

    def network_bits_needed(self, input_network_value=None):
        """
        Steps Based on Networks needed
        1. Convert the number of networks that you need to binary <NB: It’s always bes®t to subtract one from the
        number of networks needed before calculating the number of bits: eg. 5 networks; 5 - 1 = 4>
        :param: int
        :return: int
        """
        network_number = input_network_value or self.networks_needed
        if network_number.isnumeric():
            network_number = int(network_number)
        else:
            raise ValueError("Invalid Address Number.")

        if network_number <= 1:
            return 0
        input_bit = len(bin(network_number - 1)[2:])
        remaining_bit = self.TOTAL_SUBNET_BIT - self.subnetmask_decimal_to_cidr()
        host_bit = remaining_bit - input_bit
        if host_bit <= 1:
            raise ValueError("Invalid Network Number")
        return input_bit

    def input_subnet_cidr_bit(self):
        """
        This is the subnet mask in cidr bit value after validation
        :return: int
        """
        input_subnetmask = self.validate_subnetmask()
        if isinstance(input_subnetmask, int):
            return input_subnetmask
        else:
            return self.subnetmask_decimal_to_cidr()

    def subnet_number_needed(self):
        """
        This calculates the new subnet mask based on the input subnet mask of the ip address
        :return: integer
        """
        network_bits_needed = self.network_bits_needed()
        subnet_number = self.input_subnet_cidr_bit() + network_bits_needed
        if subnet_number > 30 or subnet_number < 0:
            raise ValueError("Invalid Subnet Number")
        return subnet_number

    def number_of_hosts_per_network(self):
        host_bit = self.TOTAL_SUBNET_BIT - self.validate_subnetmask(self.subnet_number_needed())
        host_number = (2 ** host_bit) - 2
        return host_number

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

    def network_increment_number(self):
        increment_position = (self.subnetmask_decimal_to_cidr() + self.network_bits_needed()) % 8
        increment_number = self.bintodec_list[increment_position - 1]
        return increment_number

    def network_id(self):
        """
        Calculate and return a list of all network ids
        :return: a list
        """
        network_bits_needed = self.network_bits_needed()
        octet_max = self.OCTET_MAX_VALUE + 1
        if network_bits_needed == 0:
            return [0]

        range_increment = self.network_increment_number()

        range_list = list(range(0, octet_max, range_increment))
        return range_list

    def broadcast_id(self):
        """
        Return the last number in the ip address list
        :return: list
        """
        if self.network_bits_needed() == 0:
            return [255]
        network_id_range = self.network_id()[1:]
        network_id_range.append(256)
        broadcast_id_range = [ip_number - 1 for ip_number in network_id_range]

        return broadcast_id_range

    def host_id(self):
        """
        Calculates the valid host range per network
        :return: list
        """
        network_ips = self.network_map_ip()
        host_ip = [list(network_ips.get(network, ())) for network in range(1, len(network_ips) + 1)]

        for host_list in host_ip:
            for number in range(len(host_list)):
                if number == 0:
                    host_list[number] += 1
                elif number == 1:
                    host_list[number] -= 1

        host_ip_address = dict(enumerate(host_ip, 1))
        return host_ip_address

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

        network = self.network_id()
        broadcast = self.broadcast_id()
        network_broadcast = zip(network, broadcast)

        return dict(enumerate(network_broadcast, 1))


if __name__ == '__main__':
    ip = IPOctet('192.168.8.8', '255.255.255.128', '20')
    host_ip_range = ip.host_id()
    subnet_bit_value = ip.subnet_number_needed()
    total_hosts = ip.number_of_hosts_per_network()
    network_range = ip.network_id()
    broadcast_range = ip.broadcast_id()
    len_of_network = len(network_range)
    network_map = dict(enumerate(zip(network_range, broadcast_range), 1))
    print(f"Host IP range: {host_ip_range}")
    print(f"Network and Broadcast ID range: {network_map}")

    print(f"This is a {ip.ip_class_name()} address and there are {len_of_network} networks with {total_hosts} "
          f"valid host ip addresses per network and a subnet mask of /{subnet_bit_value}"
          f" or {'.'.join(map(str, ip.subnetmask_cidr_to_decimal(subnet_bit_value)))}")
