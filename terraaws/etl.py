import json

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