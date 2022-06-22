import re

class Functions:
    def to_dict(self, content):
        post_data_array = content.split("$")
        post_data_mark_array = re.findall(r"\$(.*?)\$",content)
        Dict = {}

        for data in post_data_array:
            if data in post_data_mark_array:
                Dict[data] = 1
            else:
                Dict[data] = 0
        print(Dict)
        return Dict