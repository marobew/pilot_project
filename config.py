class Config(object):
    SECRET_KEY = "qwerasdf"
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:1234@127.0.0.1:3306/pilot?charset=utf8"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

