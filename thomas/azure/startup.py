from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.core.exceptions import ResourceNotFoundError
import os
import base64

credential = AzureCliCredential()
subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
blob_connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]

resource_client = ResourceManagementClient(credential, subscription_id)
network_client = NetworkManagementClient(credential, subscription_id)
compute_client = ComputeManagementClient(credential, subscription_id)

RESOURCE_GROUP_NAME = "antwan_group"
LOCATION = "francecentral"
VNET_NAME = "antwan_group-vnet"
SUBNET_NAME = "antwan_group-subnet"
GALLERY_NAME = "lab1_gallery"

USERNAME = "azureuser"
PASSWORD = "Azureuser1234"

def create_rg():
    return resource_client.resource_groups.create_or_update(RESOURCE_GROUP_NAME, 
        { 
            "location": LOCATION 
        })

def create_vn():
    poller = network_client.virtual_networks.begin_create_or_update(RESOURCE_GROUP_NAME, VNET_NAME,
        {
            "location": LOCATION,
            "address_space": {
                "address_prefixes": ["10.0.0.0/16"]
            }
        })
    return poller.result()

def create_sb():
    poller = network_client.subnets.begin_create_or_update(RESOURCE_GROUP_NAME, VNET_NAME, SUBNET_NAME,
        { 
            "address_prefix": "10.0.0.0/24" 
        })
    return poller.result()

def create_ip(name):
    poller = network_client.public_ip_addresses.begin_create_or_update(RESOURCE_GROUP_NAME, name,
        {
            "location": LOCATION,
            "sku": { "name": "Standard" },
            "public_ip_allocation_method": "Static",
            "public_ip_address_version" : "IPV4"
        })
    return poller.result()

def create_ni(nic_name, sb_res, ip_addr, ip_config_name, sg_name):
    poller = network_client.network_interfaces.begin_create_or_update(RESOURCE_GROUP_NAME, nic_name, 
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
        })
    return poller.result()

def create_vm(vm_name, username, password, nic_result, disk_name, image_name, config_code):
    poller = compute_client.virtual_machines.begin_create_or_update(RESOURCE_GROUP_NAME, vm_name,
        {
            "location": LOCATION,
            "properties": {
                "hardwareProfile": {
                    "vmSize": "Standard_B1ls",
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
                "osProfile": {
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
        })
    return poller.result()

# BOTH
rg_result = create_rg() 
vnet_result = create_vn()
subnet_result = create_sb()

# BACKEND
back_addr_result = create_ip("antwan_group_back_ip")
back_nic_result = create_ni("antwan_group_back_nic", subnet_result, back_addr_result, "antwan_group_back_cfg_ip", "/subscriptions/" + str(subscription_id) + "/resourceGroups/" + str(RESOURCE_GROUP_NAME) + "/providers/Microsoft.Network/networkSecurityGroups/back-nsg") 
vm_result = create_vm("back", USERNAME, PASSWORD, back_nic_result, "back_disk", "/subscriptions/" + str(subscription_id) + "/resourceGroups/" + str(RESOURCE_GROUP_NAME) + "/providers/Microsoft.Compute/galleries/" + str(GALLERY_NAME) + "/images/back", str(base64.b64encode(bytes('#cloud-config\nruncmd:\n - cd /home/azureuser/backend/\n - export export AZURE_STORAGE_CONNECTION_STRING=\"' + str(blob_connection_string) + '\"\n - node index.js', 'utf-8')))[2:-1]) 

# FRONTEND
front_addr_result = create_ip("antwan_group_front_ip")
front_nic_result = create_ni("antwan_group_front_nic", subnet_result, front_addr_result, "antwan_group_front_cfg_ip", "/subscriptions/" + str(subscription_id) + "/resourceGroups/" + str(RESOURCE_GROUP_NAME) + "/providers/Microsoft.Network/networkSecurityGroups/front-nsg") 
vm_result = create_vm("front", USERNAME, PASSWORD, front_nic_result, "front_disk", "/subscriptions/" + str(subscription_id) + "/resourceGroups/" + str(RESOURCE_GROUP_NAME) + "/providers/Microsoft.Compute/galleries/" + str(GALLERY_NAME) + "/images/front", str(base64.b64encode(bytes('#cloud-config\nruncmd:\n - cd /home/azureuser/frontend/\n - sed -i \'2s/.*/let back_addr = \"' + str(back_addr_result.ip_address) + '\";/\' script.js\n - python3 -m http.server', 'utf-8')))[2:-1]) 
print("Deployment done. To test, go to: http://" + str(front_addr_result.ip_address) + ":8000")