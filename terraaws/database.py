from terraaws.session import BotoSession


class RDS(BotoSession):
    """
        Description.

    """

    def __init__(self, profile_name='default', region_name='us-west-2'):
        """
           DESCRIPTIOM.

           Arguments:
            None.

           Returns:
            None.

           Tips:
            None.

        """

        BotoSession.__init__(self, profile_name=profile_name, region_name=region_name)
        self.db_subnets = {}
        self.db_instances = {}


    def create_db_subnet_group(self, db_identifier, subnet_ids):
        """
           DESCRIPTIOM.

           Arguments:
            None.

           Returns:
            None.

           Tips:
            None.

        """
        rds = self.session.client('rds')
        dbsubnet = rds.create_db_subnet_group(DBSubnetGroupDescription = '{db} subnet group'.format(db=db_identifier),
                                              DBSubnetGroupName = '{db}-subnetgroup'.format(db=db_identifier),
                                              SubnetIds = subnet_ids,
                                              Tags = [{'Key': 'Name',
                                                     'Value': '{db}-subnetgroup'.format(db=db_identifier)}])
        # describe
        dbsubnet = rds.describe_db_subnet_groups(Filters=[{'Name': 'DBSubnetGroupName',
                                                           'Values': ['{db}-subnetgroup'.format(db=db_identifier)]}])

        self.db_subnets.update(dbsubnet)

        return dbsubnet

    def launch_mysql_rds(self, dbname, username, masterpwd, dbsubnetgrp, securitygroup):
        """
           DESCRIPTIOM.

           Arguments:
            None.

           Returns:
            None.

           Tips:
            None.

        """
        rds = self.session.client('rds')
        db = rds.create_db_instance(DBName=dbname,
                                    DBInstanceIdentifier=dbname,
                                    AllocatedStorage=20,
                                    DBInstanceClass='db.t2.micro',
                                    Engine='mysql',
                                    MasterUsername=username,
                                    MasterUserPassword=masterpwd,
                                    PubliclyAccessible=True,
                                    StorageType='gp2',
                                    StorageEncrypted=False,
                                    AutoMinorVersionUpgrade=True,
                                    MultiAZ=False,
                                    DBSubnetGroupName=dbsubnetgrp,
                                    VpcSecurityGroupIds=[securitygroup],
                                    Tags=[{'Key': 'Name', 'Value': dbname}])
        waiter = rds.get_waiter('db_instance_available')
        waiter.wait(DBInstanceIdentifier=db['DBInstance']['DBInstanceIdentifier'])

        # describe
        db = rds.describe_db_instances(DBInstanceIdentifier=db['DBInstance']['DBInstanceIdentifier'])

        self.db_instances.update(db)

        return db