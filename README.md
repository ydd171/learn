 myseitu、wshell 两个均为练手项目，为初学者功能实现模块，仅供学习，完成从0到1的第一步。

myseitu为python + django + dwebsocket实现网页执行shell脚本，实时显示执行输出，附带登陆，执行历史等功能模块。

wshell使用channels.generic.websocket实现命令实时输出。功能实现：
1.用户登陆功能。
2.主机管理，包括主机名，ip,端口，访问需要的pem密钥文件等信息。
3.job管理，提供在web页面编写shell脚本的功能，并提供编辑，删除，运行相关选项。
4.job执行，点击运行job，选择执行主机，通过paramiko模块将脚本传输到对应主机目录，并授权执行。
5.结果返回,通过channels模块建立websocket连接，将命令执行结果实时传输至web页面。
6.历史记录，提供查询执行记录和执行结果的功能。
7.饼状图展示数据功能。
8.版本发布流程初级功能。

vuedjango 为功能模板。通过vue + django +python实现前端查询mysql内容，并提供execl导出功能。
