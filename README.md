# sshlink
iterm2下多服务器管理，支持gbk连接

	ssh快速连接
	usage: sshlink alias|ip
		-h:帮助
			-l [alias|ip]: 查找机器


##配置文件配置

节点配置形式为 alias = user@[ip|域名]:port
port 默认为22

	[private] #组
	local = root@10.169.10.119:61122
	local2 = root@127.0.0.1
	[default2]
	local3 = user@127.0.0.1:63322
	local4 = user@127.0.0.1:63322




##服务器查找
	
	sshlink -l #查找所有节点
	sshlink -l private #查找具体节点下的服务器列表
	sshlink -l local #根据配置的alias查找服务器
	sshlink -l 127.0.0.1 #根据ip地址查找

##服务器连接
	
	sshlink local  #根据alias连接服务器
	sshlink localgbk  #用gbk编码连接local服务器
	sshlink 192.169.1.1 #用ip地址连接服务器
