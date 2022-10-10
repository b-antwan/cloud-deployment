import boto3

try:
    
    ec2 = boto3.resource('ec2')

    # Création de l'instance de backend
    instanceBackend = ec2.create_instances(
        ImageId="ami-026b57f3c383c2eec",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        SecurityGroupIds=['sg-0f08840532c087a2c',],
        KeyName='Dorian_group4',
        UserData="""
        #cloud-config

        runcmd:
            - yum update -y 
            - curl -sL "https://rpm.nodesource.com/setup_18.x" | sudo bash -
            - sudo yum -y install nodejs 
            - sudo yum -y install git
            - git install https://github.com/b-antwan/cloud-deployment
            - cd cloud-deployment/aws/app/frontend/
            - npm install
            - node server.js
        """
    )   

    # récupération de l'identifiant de l'instance backend
    backend_id = instanceBackend[0].id

    inst = ec2.Instance(id=backend_id)
    inst.wait_until_running()

    backend_ip_address = ""

    # en fonction de l'id de l'instance récupérer
    # on récupèrel'ip correspondante 
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        if( backend_id == instance.id):
            print("backend :" + instance.id, instance.instance_type,instance.public_ip_address)
            backend_ip_address = instance.public_ip_address

    instanceFront = ec2.create_instances(
        ImageId="ami-026b57f3c383c2eec",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        SecurityGroupIds=['sg-0f08840532c087a2c',],
        KeyName='Dorian_group4',
        UserData="""
        #cloud-config

        runcmd:
            - yum update -y 
            - sudo yum install git
            - git install https://github.com/b-antwan/cloud-deployment
            - cd cloud-deployment/aws/app/frontend/
            - sed -i "1c\const backaddr = \\\"http:\\/\\/""" +  backend_ip_address  + """\\\";" script.js
            - python3 -m http.server
        """
    )
    front_id = instanceFront[0].id
    
    inst = ec2.Instance(id=front_id)
    inst.wait_until_running()

    # en fonction de l'id de l'instance récupérer
    # on récupèrel'ip correspondante 
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for instance in instances:
        if( front_id == instance.id):
            print("frontend :" + instance.id, instance.instance_type,instance.public_ip_address)
            backend_ip_address = instance.public_ip_address


except Exception as e:
    print(e)