import openstack
import errno
import os


IMAGE_NAME = "d224ca33-1d62-4e5c-9e91-acc10e383674"  
FLAVOR_NAME = "m1.small"
NETWORK_NAME = "private"
KEYPAIR_NAME = "ssh_key"
SSH_DIR = '{home}/.ssh'.format(home=os.path.expanduser("~"))
PRIVATE_KEYPAIR_FILE = '{ssh_dir}id_rsa.{key}'.format(
    ssh_dir=SSH_DIR, key=KEYPAIR_NAME)


def create_keypair(conn):
    keypair = conn.compute.find_keypair(KEYPAIR_NAME)

    if not keypair:
        print("Create Key Pair:")

        keypair = conn.compute.create_keypair(name=KEYPAIR_NAME)

        print(keypair)

        try:
            os.mkdir(SSH_DIR)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e

        with open(PRIVATE_KEYPAIR_FILE, 'w') as f:
            f.write("%s" % keypair.private_key)

        os.chmod(PRIVATE_KEYPAIR_FILE, 0o400)

    return keypair


def create_server(conn, server_name, security_group):
    
    image = conn.compute.find_image(IMAGE_NAME)
    flavor = conn.compute.find_flavor(FLAVOR_NAME)
    network = conn.network.find_network(NETWORK_NAME)
    keypair = create_keypair(conn)
    print(image)
    server = conn.compute.create_server(
        name=server_name, image_id=image.id, flavor_id=flavor.id,
        networks=[{"uuid": network.id}], key_name=keypair.name,
    )
    server = conn.compute.wait_for_server(server)

    conn.compute.add_security_group_to_server(server, security_group=add_security_group(conn, "SSH"))
    conn.compute.add_security_group_to_server(server, security_group=add_security_group(conn, security_group))
    conn.compute.add_floating_ip_to_server(server, get_floating_ip(conn))
    return server

def add_security_group(conn, security_group_name):
    security_group = conn.network.add_security_group(security_group_name)
    return security_group

def create_rule_ssh(port, security_group_id):
    return conn.network.create_security_group_rule(direction="ingress",ether_type="IPv4",port_range_min=port, port_range_max=port,protocol="tcp", security_group_id=security_group_id)


def create_security_group_ssh(conn):
    security_group = conn.network.create_security_group(name="SSH")
    security_group_rule = create_rule_ssh(22, security_group.id)
    return security_group


def get_network_id(network_name):
    network = conn.network.find_network(network_name)
    return network.id


def create_floating_ip(conn):
    id = get_network_id(network_name="public")
    ip = conn.network.create_ip(floating_network_id=id)
    return ip.floating_ip_address


def get_floating_ip(conn):
    if conn.network.find_available_ip() is None:
        return create_floating_ip(conn)
    return conn.network.find_available_ip().floating_ip_address


def create_connection_from_config():
    return openstack.connect(cloud="engines")

def list_servers(conn):
    print("listing servers..")
    for server in conn.compute.servers():
        print(server)


if __name__ == '__main__':
    conn = create_connection_from_config()
    front_server = create_server(conn=conn, server_name="test", security_group='SSH')
    front_server = conn.compute.find_server(front_server.id)
   

    