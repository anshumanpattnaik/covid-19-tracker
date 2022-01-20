import json


class JSONEntity:

    def __repr__(self):
        return self.json_str()

    def __getitem__(self):
        pass

    @classmethod
    def object(cls, data):
        if data is not None:
            result = []
            if isinstance(data, list):
                for item in data:
                    result.append(cls.object(item))
            else:
                result = cls(**data)
            return result

    def json_str(self):
        return json.dumps(self.__dict__, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def json(self):
        return json.loads(self.json_str())
