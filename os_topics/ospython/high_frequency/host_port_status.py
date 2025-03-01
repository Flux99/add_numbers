#3.Reading from STDIN and receiving two parameters which was host and ports that I need to reach and print status,what if this input is the file with 1tb(here interaction with large inputs & optimization)
# write both the function to read from arg and also from file 
import csv
import socket


def parse(path):
    with open(path) as file:
        return list(csv.reader(file, delimiter=' '))


def clean_string(s: str) -> str:
    return s.replace("'", '').replace('"', '').replace(':', '')


def connect_and_check(path):
    with socket.socket() as sock:
        rows = parse(path)
        host_port_tuples = [tuple(clean_string(s) for s in row) for row in rows]
        for host, port in host_port_tuples:
            result = sock.connect_ex((host, int(port)))
            print(f"Connection to {host} is {'OPEN' if result == 0 else 'NOT OPEN'} on Port {port}")


def test():
    """
    >>> connect_and_check('data/ipaddressrouter.txt')
    Connection to 172.217.163.164 is OPEN on Port 80
    Connection to 192.168.1.0 is NOT OPEN on Port 22
    """


if __name__ == '__main__':
    import doctest

    doctest.testmod()
