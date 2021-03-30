from terraaws.session import BotoSession

class Storage(BotoSession):
    """
        Class for boto3 AWS session.

    """
    def __init__(self, profile_name = 'default', region_name = 'us_west-2'):
        """
           The constructor for BotoSession class.
           Arguments:
               None.
           Returns:
               None.
           Tips:
           None.
        """
        self.profile_name = profile_name
        self.region_name = region_name
        self.session = boto3.Session(profile_name = profile_name, region_name = region_name)



s3 = bsm.client('s3')
bucket = s3.create_bucket(ACL='private', Bucket='tripoli-env',
                          CreateBucketConfiguration = {'LocationConstraint': 'us-west-2'})