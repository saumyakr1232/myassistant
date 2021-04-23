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

    def update(self, file_name, value, section='default'):
        try:
            with open(file_name, 'r') as f:
                doc = yaml.full_load(f)

            with open(file_name, 'w') as f:
                if doc is None:
                    doc = {section:value}
                else:
                    if doc.get(section, None) is None:
                        doc[section] = value
                    else:
                        for key in value.keys():
                            doc[section][key] = value[key]


                yaml.dump(doc, f)

        except Exception as e:
            print(e)
            return False


if __name__ == '__main__':
    obj = ConfigParser_manager()

    dic = {'per':0, 'der':1}
    obj.update('Test.yaml', dic, section='test')
    dic2 = obj.read('Test.yaml')
    print("after update")
    print(dic2)
