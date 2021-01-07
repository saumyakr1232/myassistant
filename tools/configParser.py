import yaml


class ConfigParser_manager:
    def read(self, file_name, section=''):
        try:
            with open(file_name, 'r') as f:
                documents = yaml.full_load(f)
                if section != '':
                    return documents[section]
                return documents
        except:
            return ''

    def update(self, file_name, value, section='user'):
        try:

            with open(file_name, 'r') as f:
                doc = yaml.full_load(f)

            with open(file_name, 'w') as f:
                doc[section] = value

                yaml.dump(doc, f)

        except Exception as e:
            print(e)
            return False


if __name__ == '__main__':
    obj = ConfigParser_manager()
    section = 'demo'
    dic = obj.read('Test.yaml', section=section)
    print(dic)
    dic['saumya'] = 'glo'
    obj.update('Test.yaml', dic, section=section)
    dic2 = obj.read('Test.yaml', section=section)
    print("after update")
    print(dic2)
