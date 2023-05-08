



### 改变模型需要三步

编辑 `models.py` 文件，改变模型。
运行 `python manage.py makemigrations` 为模型的改变生成迁移文件。
运行 `python manage.py migrate` 来应用数据库迁移。

### 交互式 Python 命令行

`python manage.py shell`