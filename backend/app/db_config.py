TORTOISE_ORM = {
    "connections": {
        "default": {
            'engine': 'tortoise.backends.mysql',  # MySQL or Mariadb
            'credentials': {
                'host': '127.0.0.1',
                'port': '3306',
                'user': 'root',
                'password': 'xxx',
                'database': 'examinations',
                'minsize': 1,
                'maxsize': 5,
                'charset': 'utf8mb4',
                'echo': True
            }
        }
    },
    "apps": {
        "models": {
            "models": ["app.api.models.students", "aerich.models"],
            #  your_models_path: 例如my_api.models;
            # aerich.models必须要有，但不用创建对应的models文件
            "default_connection": "default",
        }
    },
    "use_tz": False,  # 建议不要开启，不然存储日期时会有很多坑，时区转换在项目中手动处理更稳妥。
    "timezone": "Asia/Shanghai"
}
