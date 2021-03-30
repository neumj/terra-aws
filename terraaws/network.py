from terraaws.session import BotoSession
from terraaws.utilities import Network

class VPC(BotoSession):
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
        self.subnets = {}
        self.security_groups = {}
        self.route_tables = {}
        self.gateway = {}


    def create_base_vpc(self, cidr, name):
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
        # vpc
        vpc = ec2.create_vpc(CidrBlock = cidr,
                             TagSpecifications=[{'ResourceType': 'vpc', 'Tags': [{'Key': 'Name', 'Value': name + '-vpc'}]}])
        vpc_id = vpc['Vpc']['VpcId']
        waiter = ec2.get_waiter('vpc_available')
        waiter.wait(VpcIds=[vpc_id])
        _ = ec2.modify_vpc_attribute(VpcId = vpc_id,
                                     EnableDnsHostnames = {'Value': True})

        # default security group, open internal traffic
        ip22 = Network.get_public_ip() + '/32'
        sg = ec2.describe_security_groups(Filters=[{'Name': 'vpc-id' ,'Values': [vpc_id]}])
        sg_id = sg['SecurityGroups'][0]['GroupId']
        sg_tag = name + '-base-securitygroup'
        int_sg_tag = ec2.create_tags(Resources=[sg_id], Tags=[{'Key': 'Name', 'Value': sg_tag}])
        ingress = ec2.authorize_security_group_ingress(GroupId=sg_id,
                                                       IpPermissions=[
                                                           {'IpProtocol': 'tcp',
                                                            'FromPort': 80,
                                                            'ToPort': 80,
                                                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                                                           {'IpProtocol': 'tcp',
                                                            'FromPort': 443,
                                                            'ToPort': 443,
                                                            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                                                           {'IpProtocol': 'tcp',
                                                            'FromPort': 22,
                                                            'ToPort': 22,
                                                            'IpRanges': [{'CidrIp': ip22}]}
                                                       ])

        # default route table
        rt = ec2.describe_route_tables(Filters=[{'Name': 'vpc-id' ,'Values': [vpc_id]}])
        rt_id = rt['RouteTables'][0]['Associations'][0]['RouteTableId']
        rt_tag = name + '-routetable'
        rt_tbl_tag = ec2.create_tags(Resources=[rt_id], Tags=[{'Key': 'Name', 'Value': rt_tag}])

        # describe
        vpc = ec2.describe_vpcs(VpcIds=[vpc_id])
        sg = ec2.describe_security_groups(Filters=[{'Name': 'vpc-id' ,'Values': [vpc_id]}])
        rt = ec2.describe_route_tables(Filters=[{'Name': 'vpc-id' ,'Values': [vpc_id]}])

        self.vpc_id = vpc_id
        self.security_groups.update(sg)
        self.route_tables.update(rt)

        return vpc, sg, rt


    def create_subnet(self, cidr, az, name, public=False):
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
        subnet = ec2.create_subnet(VpcId = self.vpc_id,
                                   CidrBlock=cidr,
                                   AvailabilityZone=az,
                                   TagSpecifications=[{'ResourceType': 'subnet', 'Tags': [{'Key': 'Name', 'Value': name}]}])
        # auto assign ip
        if public == True:
            pub_sub = ec2.modify_subnet_attribute(SubnetId=subnet['Subnet']['SubnetId'],
                                                  MapPublicIpOnLaunch={'Value': True})

        # describe
        subnet = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [self.vpc_id]}])

        self.subnets.update(subnet)

        return subnet


    def create_internet_gateway(self, name):
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
        ig = ec2.create_internet_gateway(
            TagSpecifications=[{'ResourceType': 'internet-gateway', 'Tags': [{'Key': 'Name', 'Value': name}]}])
        ig_attach = ec2.attach_internet_gateway(InternetGatewayId = ig['InternetGateway']['InternetGatewayId'],
                                                VpcId = self.vpc_id)

        # describe
        ig = ec2.describe_internet_gateways(Filters=[{'Name': 'attachment.vpc-id',
                                     'Values': [self.vpc_id]}])

        self.gateway.update(ig)

        return ig


    def create_internet_route(self, cidr):
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
        rt = ec2.create_route(RouteTableId = self.route_tables['RouteTables'][0]['RouteTableId'],
                              DestinationCidrBlock = cidr,
                              GatewayId = self.gateway['InternetGateways'][0]['InternetGatewayId'])
        # describe
        rt = ec2.describe_route_tables(RouteTableIds = [self.route_tables['RouteTables'][0]['RouteTableId']])

        self.route_tables.update(rt)

        return rt