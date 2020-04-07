import pymongo
from webargs.flaskparser import FlaskParser
import re


myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mytable = myclient['test2m']
mycol2 = mytable['infor']
parser = FlaskParser()

ALOWED_EXTENTIONS_IMG = {'png', 'jpg', 'jpeg', 'gif'}

PATH_AVATAR = r'/Users/mf840/Desktop/facereco/template/avatars/'

URL_SERVER = "mongodb://bootai:1234567aA%40@27.72.147.222:27017"

PATH_AVATAR_SERVER = URL_SERVER + '/avatars'

AVATAR_DEFAULT = 'Avatar_Default.jpg'


def allow_file_img(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALOWED_EXTENTIONS_IMG


def parse_req(argmap):
    """

    :param argmap:
    :return:
    """
    return parser.parse(argmap)


def check_email(email):
    return re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", email)


