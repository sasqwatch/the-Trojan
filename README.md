# BlackPearl: the-Trojan
a trojan with a few modules.
程序需要设置操作邮箱和监控邮箱，
操作邮箱需提供密码并开启pop/smtp服务，用于程序接受指令和返回结果
监控邮箱只需要提供地址，用于接收返回结果

程序每五秒钟刷新一次操作邮箱，检查操作邮箱的邮件
若检测到预设的邮件标题的邮件则执行相应操作，并将结果返回boss邮箱
p.s. 邮件标题有且仅有预设命令才能执行

目前集成以下功能：
Function1：屏幕截图
  预设指令：screenCAP
  返回：保存截图并存储到d:/00.jpg，同时以附件形式立即发送至boss邮箱
Function2：ip及主机名检测
  预设指令：checkIP
  返回：主机名称以及当前ip地址
