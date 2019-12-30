import logging


class Config(object):
    """项目配置"""

    SECRET_KEY = "iECgbYWReMNxkRprrzMo5KAQYnb2UeZ3bwvReTSt+VSESW0OB8zbglT+6rEcDW9X"

    # 为数据库添加配置
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1202@.com@127.0.0.1:3306/tiktok"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 在请求结束时候，如果指定此配置为 True ，那么 SQLAlchemy 会自动执行一次 db.session.commit()操作
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # 设置日志等级
    LOG_LEVEL = logging.DEBUG


class DevelopmentConfig(Config):
    """开发环境"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境"""
    DEBUG = False
    LOG_LEVEL = logging.WARNING


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

