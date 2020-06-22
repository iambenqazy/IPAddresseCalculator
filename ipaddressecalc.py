# Calculate Classfull Addresses
import sys


class IPOctect:

    def __init__(self, ip_address, subnet_mask=24):
        self.ip_address = ip_address
        self.subnet_mask = subnet_mask
        self.octet_range = list(range(0, 256))
        self.ip_address_list = self.ip_address.split('.')

    def check_octet_range(self):
        if len(self.ip_address_list) == 4:
            for ip_index, address in enumerate(self.ip_address_list, start=1):
                try:
                    address = int(address)
                except ValueError:
                    print(f"Please enter an integer number at octet {ip_index}")
                    sys.exit()
                if address not in self.octet_range:
                    return ip_index

            return self.ip_address_list
        else:
            print("The IP address range is more or less than 4 octet")
            sys.exit()

    def ip_class_name(self):
        pass

    def netmask_id(self):
        subnet_range = list(range(1, 33))
        octet1 = subnet_range[0:8]
        octet2 = subnet_range[8:16]
        octet3 = subnet_range[16:24]
        octet4 = subnet_range[24:32]

        self.check_octet_range()
        if self.subnet_mask in octet1:
            return "Class A"
        elif self.subnet_mask in octet2:
            return "Class B"
        elif self.subnet_mask in octet3:
            return "Class C"
        elif self.subnet_mask in octet4:
            return "Class D"

    def host_id(self, name='valid'):
        host_bit = 32 - self.subnet_mask
        host_number = 2 ** host_bit
        ip_address_range = list(range(0, host_number))
        valid_host_ip = ip_address_range[1:-1]

        if name == 'ip_address_range':
            for number in ip_address_range:
                yield number
        else:
            for number in valid_host_ip:
                yield number

    def network_id(self):
        network_ip = list(self.host_id('ip_address_range'))
        return network_ip[0]

    def broadcast_id(self):
        broadcast_ip = list(self.host_id('ip_address_range'))[-1]
        return broadcast_ip

    def join_ip_address(self):
        if self.check_octet_range() is not None and not isinstance(self.check_octet_range(), int):
            ip_list = '.'.join(self.check_octet_range()[:3])
            return ip_list
        else:
            print(f"The number at octet {ip.check_octet_range()} not in range")
            sys.exit()


def networks_needed(number):

    """
    Steps Based on Networks needed 1. Convert the number of networks that you need to binary <NB: It’s always best to
    subtract one from the number of networks needed before calculating the number of bits: eg. 5 networks; 5 - 1 = 4>
    2. Reserve bits in the mask and find your increment 3. Use increment to generate networks ranges
    """
    pass


if __name__ == '__main__':
    ip = IPOctect('74.158.45.23')
    host_ip_range = [number for number in ip.host_id()]

    print(f"This is a {ip.netmask_id()} address and there are {len(host_ip_range)} valid host ip addresses starting from {ip.join_ip_address()}.{host_ip_range[0]} to {ip.join_ip_address()}.{host_ip_range[-1]}")
    print(f"The network id is {ip.join_ip_address()}.{ip.network_id()}")
    print(f"The broadcast id is {ip.join_ip_address()}.{ip.broadcast_id()}")
