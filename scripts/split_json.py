import cPickle
import json
from os.path import dirname, abspath,join
try:
    with  open('crawler/items.json', "r") as json_dump:
        json_data = json.load(json_dump)
        json_dump.close()
    a = [saved_data for saved_data in json_data if str(saved_data).startswith("{u'ch")]
    with open(join(dirname(abspath(dirname(__file__))),'tbc_error_page/error.pickle'), "w+") as error_json:
        cPickle.dump(a, error_json)
        error_json.close()

    b = [saved_data for saved_data in json_data if str(saved_data).startswith("{u'br")]
    with open(join(dirname(abspath(dirname(__file__))),'tbc_error_page/broken.pickle'), "w+") as broken_json:
        cPickle.dump(b, broken_json)
        broken_json.close()


except ValueError:
    print "Couldn't find file"
