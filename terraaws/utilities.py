import re
import urllib.request as req
import json
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
                                                      Body = (bytes(json.dumps(object).encode('UTF-8'))),
                                                      Key = object_key)

        return s3_object


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