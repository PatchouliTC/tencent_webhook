# TencentGit_WebHookRobotService

## 目标
 实现一个面向腾讯工蜂的webhook机器人服务
 
 该服务提供多存储库监听，基本信息本地快照存储，定时数据统计，多接收端发送等功能

 当前预计提供push,merge信息监听

## 部署
### 设置环境与执行
1. 为项目设置虚拟环境---[ virtualenv或者通过conda创建相关虚拟环境 ]
2. 进入虚拟环境，根据项目`requirements.txt`执行`pip install -r requirements.txt`安装需要的依赖库
3. [可选]编辑`alembic.ini` 的sqlalchemy.url来指定数据库[当前默认使用sqlite3],并同时修改对应`AppSettings`中SQL_URL地址
3. 在项目根目录下执行`alembic revision --autogenerate` 和 `alembic upgrade head`生成数据库
3. 项目根目录下的`boot.sh`中在7~9行中添加对应虚拟环境激活方式
4. 设置完毕后在根目录的`AppSettings.pro`中修改需要的配置信息用于生产环境[配置详情在下方提供]
5. 执行`bash boot.sh`即可启动该服务功能

### 配置文件详情
- APP_NAME 标记该服务名称
- PORT 指定服务监听端口
- HOST 指定服务监听地址[localhost or 0.0.0.0]
- DEBUGMODE 是否以debug模式启动
- DEVELOP 是否以开发模式启动[仅在开发模式下swagger接口文档可访问]
- ROBOTHOOKURL 指定接收到Hook后转发目标机器人的URL地址[DEV适用]
- ACCESSTOKEN 获取相关GIT端信息时需要的访问token[DEV适用],没有该token将无法获取相关提交细节信息
- SENDTIME 指定每日何时发送通知信息[DEV适用]
- AUTOADDUNKNOWNREPO 当有未定义存储库hook访问时是否自动创建对应的存储库
- SQL_URL 指定数据库,URL中需要包含用户密码等信息
- LOG_FILE_ROOT_PATH 指定日志保存位置与文件名，无绝对路径则保存于当前项目下[即相对路径]

### 启动命令行参数详情
python setup.py run -n <override APPName> -c <APPSettingFilePath> -d[Run as DEBUGMODE] -p <Port>
[命令行参数优先级高于配置文件中对应值,即如果存在命令行参数，则会覆盖配置文件中对应的值配置]
- -n 指定APP名称
- -c 指定配置文件位置
- -d 强制以debug模式启动
- -p 强制监听目标端口 

### 接口文档信息
以develop配置文件启动服务，在<host>:<port>/docs下即可查看相关接口信息
