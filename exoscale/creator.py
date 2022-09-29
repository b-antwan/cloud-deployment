import exoscale
from exoscale.api.compute import SSHKey
exo = exoscale.Exoscale()


zone_gva2 = exo.compute.get_zone("ch-gva-2")

# Image/template for the modules

front_template = exo.compute.get_instance_template(
    zone_gva2, "ecbcdd9a-3642-4335-b84e-d86f0dd065b7")

back_template = exo.compute.get_instance_template(
    zone_gva2, "d9f65174-ac81-40f9-9448-cf64af1f3bcb")


print("Creating Backend")
# Create backend instance
back = exo.compute.create_instance(name="back",
                                    zone=zone_gva2,
                                   type=exo.compute.get_instance_type("tiny"),
                                   template=back_template,
                                   security_groups=[exo.compute.get_security_group(
                                       id="f563ae78-ba19-4a4d-becc-0c4e8d73bea7"),
                                       exo.compute.get_security_group(
                                        id="a9bdca8b-9ac1-41c5-bbad-0b38a62cfe80")],
                                   user_data="""
                                    #cloud-config
                                    runcmd:
                                    - cd /home/ubuntu/backend/ 
                                    - node index.js
                                """)

print("Backend has been created on ip. " + str(back.ipv4_address))

print("Creating Frontend")
# Create frontend instance
front = exo.compute.create_instance(name="front",
                                    zone=zone_gva2,
                                    type=exo.compute.get_instance_type("tiny"),
                                    template=front_template,
                                    security_groups=[exo.compute.get_security_group(
                                        id="c7c3403f-3d08-4b21-a4c7-8ac4a144ddd3"),
                                        exo.compute.get_security_group(
                                        id="a9bdca8b-9ac1-41c5-bbad-0b38a62cfe80")],
                                    ssh_key=exo.compute.get_ssh_key("antwan"),
                                    user_data="""
                            #cloud-config
                            runcmd:
                                - cd /home/ubuntu/frontend
                                - sed -i "1c\const backaddr = \\\"http:\\/\\/""" +  back.ipv4_address  + """\\\";" script.js
                                - python3 -m http.server
                            """)
print("Frontend has been created on ip. " + str(front.ipv4_address))