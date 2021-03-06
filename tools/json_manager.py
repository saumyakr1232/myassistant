try:
    import json
except Exception as e:
    pass


class JsonManager:
    """ It will loads data and dumps data into json."""
    @staticmethod
    def json_read(json_file):
        try:
            with open(json_file, "r") as read_file:
                data = json.load(read_file)
            return data
        except Exception as e:
            print(e)

    @staticmethod
    def json_write(json_file, data=None):
        if data is None:
            data = {}
        try:
            with open(json_file, "w") as write_file:
                json.dump(data, write_file)

            json_string = json.dumps(data)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    x = JsonManager.json_read('S:\Projects\myassistant\AI\.learnt')
    print(x)
    x.update({"alternate":"test"})
    JsonManager.json_write('S:\Projects\myassistant\AI\.learnt', x)
    x = JsonManager.json_read('S:\Projects\myassistant\AI\.learnt')
    print(x)
