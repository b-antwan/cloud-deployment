from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.core.exceptions import ResourceNotFoundError
import os
import base64

credential = AzureCliCredential()
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]

resource_client = ResourceManagementClient(credential, subscription_id)
network_client = NetworkManagementClient(credential, subscription_id)
compute_client = ComputeManagementClient(credential, subscription_id)

RESOURCE_GROUP_NAME = "banantwan_group"
LOCATION = "westeurope"
VNET_NAME = "banantwan_group-vnet"
SUBNET_NAME = "banantwan-subnet"

USERNAME = "thomas"
PASSWORD = "MySuperPassword1234"

def create_rg():
    return resource_client.resource_groups.create_or_update(RESOURCE_GROUP_NAME, {
        "location": LOCATION
    })

def create_vn(vnet_name):
    poller = network_client.virtual_networks.begin_create_or_update(RESOURCE_GROUP_NAME,
        VNET_NAME,
        {
            "location": LOCATION,
            "address_space": {
                "address_prefixes": ["10.0.0.0/16"]
            }
        }
    )
    return poller.result()

def create_sb():
    poller = network_client.subnets.begin_create_or_update(RESOURCE_GROUP_NAME, 
        VNET_NAME, SUBNET_NAME,
        { "address_prefix": "10.0.0.0/24" }
    )
    return poller.result()

def create_ip(name):
    poller = network_client.public_ip_addresses.begin_create_or_update(RESOURCE_GROUP_NAME,
        name,
        {
            "location": LOCATION,
            "sku": { "name": "Standard" },
            "public_ip_allocation_method": "Static",
            "public_ip_address_version" : "IPV4"
        }
    )
    return poller.result()

def create_ni(nic_name, sb_res, ip_addr, ip_config_name, sg_name):
    poller = network_client.network_interfaces.begin_create_or_update(RESOURCE_GROUP_NAME,
        nic_name, 
        {
            "location": LOCATION,
            "ip_configurations": [ {
                "name": ip_config_name,
                "subnet": { "id": sb_res.id },
                "public_ip_address": {"id": ip_addr.id }
            }],
            "networkSecurityGroup": {
                "id": sg_name
            }
        }
    )
    return poller.result()

def create_vm(vm_name, username, password, nic_result, disk_name, image_name, config_code):
    print(f"Provisioning virtual machine {vm_name}; this operation might take a few minutes.")
    poller = compute_client.virtual_machines.begin_create_or_update(RESOURCE_GROUP_NAME, vm_name, disk_name, image_name, config_code,
        {
            "location": LOCATION,
            "properties": {
                "hardwareProfile": {
                    "vmSize": "Standard_D1_v2",
                },
                "storageProfile": {
                    "imageReference": {
                        "id": image_name
                    },                           
                    "osDisk": {
                        "caching": "ReadWrite",
                        "managedDisk": {
                            "storageAccountType": "Standard_LRS"
                        },
                        "name": disk_name,
                        "createOption": "FromImage"
                    }
                },
                "os_profile": {
                    "computer_name": vm_name,
                    "admin_username": username,
                    "admin_password": password
                },
                "networkProfile": {
                    "networkInterfaces": [
                    {
                        "id": nic_result.id,
                        "properties": {
                            "primary": True
                        }
                    }]
                },
                "userData": config_code
            }                                                                      
        }
    )
    return poller.result()

# BOTH
rg_result = create_rg() 
vnet_result = create_vn()
subnet_result = create_sb()

# BACKEND
back_addr_result = create_ip("back_ip")
back_nic_result = create_ni("back_nic", subnet_result, back_addr_result, "back_cfg_ip", "/subscriptions/" + str(subscription_id) + "/resourceGroups/" + str(RESOURCE_GROUP_NAME) + "/providers/Microsoft.Network/networkSecurityGroups/BACK-nsg") 
vm_result = create_vm("BACK", USERNAME, PASSWORD, back_nic_result, "BACK_disk", "/subscriptions/" + str(subscription_id) + "/resourceGroups/" + str(RESOURCE_GROUP_NAME) + "providers/Microsoft.Compute/galleries/lab1_gallery/images/backend_image", str(base64.b64encode(bytes('#cloud-config\nruncmd:\n - cd /home/thomas/backend/\n - export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=cloudlab1;AccountKey=Dj7nJbfXaUy+U8+WEgfX0yB/wJ0k+havtFTLkuZIKAUuAuj+5T6wflQJ5zpQSNxUNrCfTnCZZsLe+AStlP02Vg==;EndpointSuffix=core.windows.net"\n - node server.js', 'utf-8')))[2:-1]) 

# FRONTEND
front_addr_result = create_ip("back_ip")
front_nic_result = create_ni("front_nic", subnet_result, front_addr_result, "front_cfg_ip", "/subscriptions/" + str(subscription_id) + "/resourceGroups/" + str(RESOURCE_GROUP_NAME) + "providers/Microsoft.Network/networkSecurityGroups/FRONT-nsg") 
vm_result = create_vm("FRONT", USERNAME, PASSWORD, front_nic_result, "FRONT_disk", "/subscriptions/" + str(subscription_id) + "/resourceGroups/" + str(RESOURCE_GROUP_NAME) + "providers/Microsoft.Compute/galleries/lab1_gallery/images/frontend_image", str(base64.b64encode(bytes('#cloud-config\nruncmd:\n - cd /home/thomas/frontend/\n - sed -i \'2s/.*/let back_addr = \"' + str(back_addr_result.ip_address) + '\";/\'  index.js\n - python3 -m http.server', 'utf-8')))[2:-1]) 