from flask import Flask
from flask_cors import CORS


def create_app():
    """
    创建app对象
    :return:
    """
    app = Flask(__name__,
                static_folder="./vue-project/dist/static",
                template_folder="./vue-project/dist")

    # 跨平台访问
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    return app

