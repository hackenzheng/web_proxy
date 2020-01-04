内核模块是什么及怎么编写内核模块
https://www.cnblogs.com/wrjvszq/p/4260996.html

systemtap 运行时的错误信息含义: https://www.jianshu.com/p/bb6f88c61449


https://myaut.github.io/dtrace-stap-book/tools/systemtap.html


有输出
stap -l 'process("/lib/x86_64-linux-gnu/libc.so.6").function("printf")'


没有输出
stap -l 'kernel.function("sys_recv")'

官方编译的 MySQL 不支持 mark 观测点,自己编译的是会有输出的
stap -v -L 'process("/usr/sbin/mysqld").mark("*")'
stap -L 'process("/usr/sbin/mysqld").function("main")'

stap -l 'probe process("/usr/local/mysql/bin/mysqld").function("query__parse__start")'

源码编译安装 MySQL: https://www.jianshu.com/p/117dab1b658d,最后执行下面的命令 cmake, cmake 也需要sudo
cmake . -DBUILD_CONFIG=mysql_release -DCPACK_MONOLITHIC_INSTALL=ON -DCMAKE_INSTALL_PREFIX=/usr/local/mysql -DDEFAULT_CHARSET=utf8 -DDEFAULT_COLLATION=utf8_general_ci -DMYSQLX_TCP_PORT=33060 -DMYSQL_UNIX_ADDR=/usr/local/mysql/mysql.sock -DMYSQL_TCP_PORT=3306 -DMYSQLX_UNIX_ADDR=/usr/local/mysql/mysqlx.sock -DMYSQL_DATADIR=/usr/local/mysql/data -DSYSCONFDIR=/usr/local/mysql/etc -DENABLE_DOWNLOADS=ON -DWITH_BOOST=system -DENABLE_DTRACE=on 
-DWITH_DEBUG=1

安装后的路径是 /usr/local/mysql/bin
 root@localhost: 2a.rYG,.r1hE
 
  sudo /usr/local/mysql/support-files/mysql.server start
  
  
  
global latency
probe process("/usr/local/mysql/bin/mysqld").mark("query__parse__start") {
        printf ("parsing %s\n", user_string($arg1))
        latency[tid()] = gettimeofday_ns()
}
 
probe process("/usr/local/mysql/bin/mysqld").mark("query__parse__done") {
        printf ("parse latency: %dns\n", gettimeofday_ns() - latency[tid()])
}


SystemTap是Redhat推出的，如果服务器是Redhat，那么是不需要安装的


很全的系统监测工具介绍:
https://www.cnblogs.com/tcicy/p/8461807.html


Linux 给我们提供的数据源包括操作系统内核态提供的观测点和用户态提供的观测点，MySQL 很早之前就提供了用户态的观测点。
https://juejin.im/entry/5bac3addf265da0af93b08ae

systemtap语法
https://yq.aliyun.com/articles/174916?utm_content=m_28902


阿里 对应的 ppt https://myslide.cn/slides/16513


top 命令输出
https://blog.csdn.net/lv_xinmy/article/details/8574226