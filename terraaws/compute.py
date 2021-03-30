from terraaws.session import BotoSession

class EC2(BotoSession):
    """
        Description.

    """

    def __init__(self, profile_name='default', region_name='us-west-2'):
        """
           Desription.
           Arguments:
               None.
           Returns:
               None.
           Tips:
           None.
        """
        BotoSession.__init__(self, profile_name = profile_name, region_name = region_name)
        self.instances = {}


    def create_key(self, key_name, path):
        """
           Desription.
           Arguments:
               None.
           Returns:
               None.
           Tips:
           None.
        """
        ec2 = self.session.client('ec2')
        priv_key = ec2.create_key_pair(KeyName = key_name)
        key_file = open(path + os.sep + key_name + '.pem', "w")
        f = key_file.write(priv_key['KeyMaterial'])
        key_file.close()

        return priv_key


    def launch_amazon_linux2(self, name, subnet_id, security_groups, key_name,
                             itype='t2.micro', ami='ami-05b622b5fa0269787'):
        """
           Desription.
           Arguments:
               None.
           Returns:
               None.
           Tips:
           None.
        """
        ec2 = self.session.client('ec2')
        instance = ec2.run_instances(ImageId=ami,
                                     InstanceType=itype,
                                     MaxCount=1,
                                     MinCount=1,
                                     SubnetId=subnet_id,
                                     BlockDeviceMappings=[{'DeviceName': '/dev/xvda',
                                                           'VirtualName': name + '-storage',
                                                           'Ebs': {'DeleteOnTermination': True,
                                                                   'VolumeSize': 30}
                                                           }],
                                     TagSpecifications=[{'ResourceType': 'instance',
                                                         'Tags': [{'Key': 'Name', 'Value': name}]}],
                                     SecurityGroupIds=security_groups,
                                     KeyName=key_name)
        waiter = ec2.get_waiter('instance_status_ok')
        waiter.wait(InstanceIds=[instance['Instances'][0]['InstanceId']])

        # describe
        instance = ec2.describe_instances(InstanceIds=[instance['Instances'][0]['InstanceId']])

        self.instances.update(instance)

        return instance