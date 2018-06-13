#!/bin/bash
#####		一键初始化Linux			#####
#####		Author:bopy				#####
#####		Update:2018-06-13		#####


function CentOS()
{
	yum install -y git
	yum install -y screen
	yum install -y ctags
	yum install -y ncurses
	yum install -y ncurses-libs
	yum install -y ncurses-devel

}

function Ubuntu()
{
	########## Base Setting ###########
	# set host name
	sudo hostnamectl set-hostname wwsbbase_cd
	# set PS1
	echo "export PS1='\n\e[1;37m[\e[m\e[1;34m\u\e[m\e[1;37m@\e[m\e[1;31m\H\e[m \e[4m`pwd`\e[m\e[1;37m]\e[m\e[1;36m\e[m\n\$'" >> $HOME/.bashrc

	# install base tools
	sudo apt-get install -y  git
	sudo apt-get install -y  screen
	sudo apt-get install -y  ctags
	sudo apt-get install -y  python-dev
	sudo apt-get install -y  libncurses5-dev
	sudo apt-get install -y  wget
	sudo apt-get install -y  unzip
	sudo apt-get install -y  gcc
	sudo apt-get install -y  dstat

	############## Vim ################
	# get latest vim src code 
	git clone https://github.com/vim/vim.git
	cd vim
	git pull
	
	# clean 
	make distclean  # if you build Vim before
	
	# get python path
	python_lib_path="/usr/lib64/python2.7/config/"
	
	# install
	./configure --with-features=huge --enable-pythoninterp=yes --enable-rubyinterp=yes --enable-luainterp=yes --enable-perlinterp=yes --with-python-config-dir=$python_lib_path --enable-gui=gtk2 --enable-cscope --prefix=/usr/local
	
	make
	sudo make install

	# config
	git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim

	wget https://codeload.github.com/wwsbbase/vimrc_settings/zip/master

	unzip master && cd vimrc_settings-master && cp vimrc $HOME/.vimrc

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