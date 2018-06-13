#!/bin/bash
#####		一键初始化Linux			#####
#####		Author:bopy				#####
#####		Update:2018-06-13		#####


function CentOS()
{
	yum install git
	yum -y install screen
	apt-get -y install ctags
	
	yum install ncurses
	yum install ncurses-libs
	yum install ncurses-devel

}

function Ubuntu()
{

	sudo apt-get -y install git
	sudo apt-get -y install screen
	sudo apt-get -y install ctags
	
	sudo apt-get -y install libncurses5-dev


	git clone https://github.com/vim/vim.git
	cd vim
	git pull
	
	
	make distclean  # if you build Vim before
	
	# get python path
	python_lib_path="/usr/lib64/python2.7/config/"
	
	./configure --with-features=huge --enable-pythoninterp=yes --enable-rubyinterp=yes --enable-luainterp=yes --enable-perlinterp=yes --with-python-config-dir=$python_lib_path --enable-gui=gtk2 --enable-cscope --prefix=/usr/local
	
	make
	sudo make install
	

}

function Debian()
{
	echo "Debian"
}


echo '#####		欢迎使用一键初始化Linux脚本^_^	#####'
echo '----------------------------------'
echo '请选择系统:'
echo "1) CentOS 7 X64"
echo "2) Ubuntu 14+ X64"
echo "3) Debian 8+ X64"
echo "q) 退出"
echo '----------------------------------'
read -p ":" num
echo '----------------------------------'

case $num in
	1)
		#安装
		CentOS
		#设置
		#setting $osip
		exit
	;;
	2)
		#安装aria2
		Ubuntu
		#setting $osip
		exit
	;;
	3)
		Debian
		#setting $osip
		#echo "温馨提示：Debian/Ubuntu用户若无法访问，需要放行 6080/6800/51413 端口或关闭防火墙！"
		#echo '----------------------------------'
		exit
	;;
	q)
		exit
	;;
	*)
		echo '错误的参数'
		exit
	;;
esac