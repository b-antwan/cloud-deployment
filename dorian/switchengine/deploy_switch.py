from re import sub
import openstack
import errno
import os
import subprocess
import base64

IMAGE_NAME = "Ubuntu Bionic 18.04 (SWITCHengines)"  
FLAVOR_NAME = "m1.small"
NETWORK_NAME = "private"
KEYPAIR_NAME = "ssh_key"
SSH_DIR = '{home}/.ssh/'.format(home=os.path.expanduser("~"))
PRIVATE_KEYPAIR_FILE = '{ssh_dir}ssh_key.pem'.format(
    ssh_dir=SSH_DIR)


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


def create_server(conn, server_name,my_keypair):
    
    image = conn.compute.find_image(IMAGE_NAME)
    flavor = conn.compute.find_flavor(FLAVOR_NAME)
    network = conn.network.find_network(NETWORK_NAME)
    keypair = my_keypair
    
    
    server = conn.compute.create_server(
        name=server_name, image_id=image.id, flavor_id=flavor.id,
        networks=[{"uuid": network.id}], key_name=keypair.name, security_groups = [{"name": "ssh"}], 	
    )
    server = conn.compute.wait_for_server(server)
    ip = get_floating_ip(conn)
    conn.compute.add_floating_ip_to_server(server, ip)
    
    return server,ip

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
    my_keypair = create_keypair(conn)
    back_server = create_server(conn=conn, server_name="Back",my_keypair=my_keypair)
    ip_back = back_server[1]
    print("Backend instance IP :" + ip_back)
    print("scp -r -i ~/.ssh/ssh_key.pem ./app/backend/ ubuntu@" + ip_back+ ":")
    
    front_server = create_server(conn=conn, server_name="Front",my_keypair=my_keypair)
    ip_front = front_server[1]
    print("Frontend instance IP :" + ip_front)
    p2 = subprocess.Popen('sed -i "1c\const backaddr = \\\"http:\\/\\/' +  ip_back  + '\\\";" ./app/frontend/script.js',shell=True)
    sts2 = p2.wait()
    print("scp -r -i ~/.ssh/ssh_key.pem ./app/frontend/ ubuntu@" + ip_front+ ":")
    print()
    
    
