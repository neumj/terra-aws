import re
import urllib.request as req
import json
import datetime
from terraaws.session import BotoSession


class S3(BotoSession):
    """
        Class for boto3 AWS session.

    """

    def __init__(self, profile_name='default', region_name='us-west-2'):
        """
           The constructor for BotoSession class.
           Arguments:
               None.
           Returns:
               None.
           Tips:
           None.
        """
        BotoSession.__init__(self, profile_name = profile_name, region_name = region_name)


    def create_private_bucket(self, bucket_name):
        """
           DESCRIPTIOM.

           Arguments:
            None.

           Returns:
            None.

           Tips:
            None.

        """
        bucket = self.session.client('s3').create_bucket(ACL='private', Bucket=bucket_name,
                                                         CreateBucketConfiguration={'LocationConstraint': self.region_name})

        return bucket


    def put_object(self, object, bucket_name, object_key):
        """
           DESCRIPTIOM.

           Arguments:
            None.

           Returns:
            None.

           Tips:
            None.

        """
        s3_object = self.session.client('s3').put_object(ACL = 'private',
                                                      Bucket = bucket_name,
                                                      Body = (bytes(json.dumps(object, default=self.datetime_handler).encode('UTF-8'))),
                                                      Key = object_key)

        return s3_object


    def datetime_handler(self, x):
        if isinstance(x, datetime.datetime):
            return x.isoformat()
        raise TypeError("Unknown type")


class Network():
        """
            Class for network utilities.

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
            pass


        def get_public_ip():
            """
               DESCRIPTIOM.

               Arguments:
                None.

               Returns:
                None.

               Tips:
                None.

            """
            data = str(req.urlopen('http://checkip.dyndns.com/').read())

            return re.compile(r'Address: (\d+.\d+.\d+.\d+)').search(data).group(1)


        def get_subnet_id(subnets_response, subnet_name):
            """
               DESCRIPTIOM.

               Arguments:
                None.

               Returns:
                None.

               Tips:
                None.

            """
            for sn in subnets_response['Subnets']:
                for t in sn['Tags']:
                    if t['Value'] == subnet_name:
                        return (sn['SubnetId'])


        def get_securitygroup_id(securitygroups_response, securitygroup_name):
            """
               DESCRIPTIOM.

               Arguments:
                None.

               Returns:
                None.

               Tips:
                None.

            """
            for sg in securitygroups_response['SecurityGroups']:
                for t in sg['Tags']:
                    if t['Value'] == securitygroup_name:
                        return(sg['GroupId'])


class JSON():
    """
        Class for JSON handling.

    """
    def __init__(self):
        """
           The constructor for Json class.
           Arguments:
               None.
           Returns:
               None.
           Tips:
           None.
        """
        pass


    def read_json(self, file_path):
        """
           Read json file.
           Arguments:
            file_path -- string, path to file.
           Returns:
            d -- dictionary, with json contents.
           Tips:
            None.
        """
        with open(file_path) as json_data:
            d = json.load(json_data)

        return d

    def write_json(self, data_dict, file_path):
        """
           Write dictionary to json.
           Arguments:
            data_dict -- dictionary.
            file_path -- string, path to file.
           Returns:
            None.
           Tips:
            None.
        """
        with open(file_path, 'w') as fp:
            json.dump(data_dict, fp, indent=4)