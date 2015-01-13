一，安装apache(假设已经安装好)
二，安装mod_python模块
    sudo apt-get install libapache2-mod-python
三，配置apache以处理mod_python程序：sudo gedit /etc/apache2/apache2.conf。(我的apache没有httpd.conf，反正找到『<Directory /var/www/>』就可以)

          把这个文件里的

          <Directory /var/www/>

                 Options Indexs FollowSymLinks

                 AllowOverride  None

                 Require  all granted

          </Directory>

         添加三句：

         

          <Directory /var/www/>

                 Options Indexs FollowSymLinks

                 AllowOverride  None

                 Require  all granted

                 AddHandler  mod_python   .py                              （这里mod_python 和.py要有一个空格）

                 PythonHandler  test           (我这里要处理的是test.py，所以加了test，不加py，而且只能加一个参数，加完后重启apache服务)

                 PythonDebug   On

          </Directory>
四，编写test.py
     在目录/var/www下：sudo   gedit /var/www/test.py，内容如下
     from mod_python import apache

     def handler(req):

          req.content_type='text/plain'

          req.write("hello,world")

          return apache.OK
     然后到浏览器输入:http://localhost/test.py

     如果在浏览器看到hello,world。那么说明一切顺利
五，说明分发程序的重要性。
      mod_python和apache的环境下游点怪。如果你在写一个hello.py：
      from mod_python import apache

      def handler(req):

          req.content_type='text/plain'

          req.write("hello，my friends")
          return apache.OK
      然后都浏览器输入:http://localhost/hello.py
      你会发现浏览器显示的是test.py的结果。为什么会这样？因为我们在配置中添加了PythonHandler  test，那么mod_python处理器只调用test.py的handler()，不管你的url是什么。那么引入分发程序很有必要，就是不管url是什么，分发程序会从url读取你要请求的.py文件，返回import相应的.py，然后调用该.py的handler
      这个分发程序我已写好，叫做dispacher2.py。你现在只需修改apache配置文件中这句『PythonHandler  test』为『PythonHandler  dispacher2』,重启apache:
      sudo /etc/init.d/apache2 restart
      然后你现在可以在浏览器实验一下，分别输入http://localhost/test.py或http://localhost/hello.py,你都会得到你想要的结果
六，准备运行
     了解这些后，把源码放入apache的环境下运行。把所有的.py文件放入/var/www下,把uploadpage.htm放入/var/www/html,如果没有这个目录，放入/var/www。接下来就是修改配置文件了,这部份前面已经介绍
七，关于源码的一些说明。这些.py文件是从贾荻写的.jsp文件改写过来的，所以大部分功能不变。但我修改了一些存放.sh文件的路径。比如在ChangParameter.py里
我让basePath="/home/youqi/Desktop/cg-rtl/testcase/"，原来的jsp文件是这样basePath="/usr/local/share/cg-rtl/testcase/"。那么我为什么那cg-rtl/testcase建在
桌面，而不是/usr/local/share。我这里试过用原来的路径。那么脚本执行会失败，会抛出没有权限建立这个文件夹，而在桌面上，我建立cg-rtl，然后chmod 777权限给这个文件夹，那么就执行成功了。
      还有一个修改的地方是我把runfile的路径定义为：runfile = "/home/youqi/Desktop/ExcuteFile/helloworld.sh"。可以看出我也是建立在桌面上，所以移植时要做相应修改。
八，源码的注释
    我为什么把源码的注释写在这，而不是源文件?是这样的，我在源码写注释时，它在本地会运行失败。说是编码错误。可能我本地虚拟机没安装中文输入法的原因吧
    ChangeParameter.py:
    from mod_python import apache,util,Session
    import os
    def handler(req,sess):  #编写处理器函数，
      basePath="/home/youqi/Desktop/cg-rtl/testcase/" 
      form = util.FieldStorage(req)    #取表单字典
      v_version=form["version"].value  #通过form字典获取version，platform，testcase的值
      v_platform=form["platform"].value
      v_testcase=form["testcase"].value
      filePath=basePath + v_testcase + "/"  #构建文件testcase的文件夹路径
      if not os.path.exists(basePath):      #basePath不存在的话，创建它
      	    os.mkdir(basePath)
      req.content_type="text/html"          #返回客户端的页面
      req.write("""<html><head><title>change parameter</title></head>
               <body>change parameter successfully!</body></html>""")
      sess["version"]=v_version             #把version，platform和filePath存到session对象中，以供夸请求的表单访问，具体来说是放后面的uploadfile.py，     
      sess["platform"]=v_platform           #ImportSymbolTable.py  ，ExcuteTestScript.py访问的v_version，v_platform ，filePath
      sess["testcase"]=filePath
      sess.save()
      return apache.OK



      UploadFile.py：
      from mod_python import apache,util,Session
      import os
      def handler(req,sess):
      maxFileSize = 5000 * 1024  #按照贾荻jsp文件中的定义
      maxMemSize = 5000 * 1024
      v_version=sess["version"]    #从session对象中获取v_version，v_platform ，filePath
      v_platform=sess["platform"]
      filePath=sess["testcase"]
      if not os.path.exists(filePath):
      	    os.mkdir(filePath)
      try:                         # 这个可能是处理从windows下上传文件时要设置的吧          
          import msvcrt
          msvcrt.setmode(0,O_BINARY)
          msvcrt.setmode(1,O_BINARY)
      except ImportError:
          pass
      form = util.FieldStorage(req)   #获取表单字典
      fileitem=form['file']	          #获取将要上传的文件信息    
      fileName=fileitem.filename      #获取文件名
      if fileName.rfind("\\")>=0:     
          fileName=fileName[fileName.rfind("\\"):]
      else:
          fileName=fileName[fileName.rfind("\\")+1:]  
      req.content_type='text/html'
      req.write("""<html><head><title>File upload</title></head><body>""")
      if fileName:
      	  dirname=fileName
      	  fileName=fileName.replace("-", "_")
      	  fileName="V-"+v_version+"P-"+v_platform+"T-"+fileName  #标准化命名
      	  sess["dirname"]=dirname
      	  sess.save()
      	  fname=os.path.basename(fileitem.filename)
          fout=open(os.path.join(filePath,fname),'wb')   #以'wb'的形式创建一个写文件
          while True:
              chunk=fileitem.file.read(100000)
              if not chunk:break
              fout.write(chunk)
          fout.close()
          v=filePath +fileName
          req.write("""<h2>Success to upload!</h2><br>   Uploaded Filename: %s<br>"""%v)
          req.write("""<a href="http://localhost/UploadPage.htm">Continue to upload</a></body></html>""")
      else:
          req.write("""No file was selected!</body></html>""") 
      return apache.OK
 
   

      ImportSymbolTable.py：

      from mod_python import apache,util,Session
      from subprocess import call
      def handler(req,sess):
          v_version=sess["version"]    #从session对象中获取v_version，v_platform ，filePath
          v_platform=sess["platform"]
          v_testcase=sess["testcase"]
          runfile = "/home/youqi/Desktop/ExcuteFile/helloworld.sh"   #运行.sh文件的路径
          req.content_type='text/html'
          req.write("""<html><head><title>JSP TestCase</title></head><body>""")
          try:
      	    cmd=["/bin/sh",runfile]    #传给将要创建的子进程的参数
            exitValue=call(cmd)        #创建子进程，结束后，把返回值赋给  exitValue  
            req.write(runfile)        
            req.write("""<br>""")
            if exitValue !=0:          #子进程不正常执行cmd命令的退出状态  
          	   req.write("""<h2>Error to excute!</h2><br>""")
            else:                      #成功执行            
          	   req.write("""<h2>Success to excute!</h2><br>""")
          except Exception,e:
      	    req.write("""Error!""")
          finally:
      	      req.write("""<h2>Finish!</h2>
      	  	</body>
      	  	</html>""")
          return apache.OK

       ExcuteTestScript.py:

from mod_python import apache,util,Session
from subprocess import call
def handler(req,sess):
      v_version=sess["version"]  #从session对象中获取v_version，v_platform ，filePath
      v_platform=sess["platform"]
      v_testcase=sess["testcase"]
      v_filename=sess["dirname"]  #这个dirname是在uploadfile.py定义的，它的值应该是fileName的内容
      runfile=""              
      req.content_type='text/html'
      req.write("""<html><head><title>JSP TestCase</title></head><body><br>""")
      try:
      	   if v_testcase.find("testcase1")!=-1:   #testcase1的runfile值
      	   	   runfile = "/home/crdong/main/a.sh"
      	   elif v_testcase.find("testcase2")!=-1: #testcase2的runfile值
               dirname=v_filename[:v_filename.index(".tar.gz")] 
               runfile="/usr/local/apache-tomcat-7.0.57/webapps/ROOT/remote.sh"
               util.redirect(req,"http://124.16.141.184:8080/mym_test/"+dirname+"/index_page.html")
           else:                                  #其余testcase的runfile值                 
               runfile = "/home/youqi/Desktop/ExcuteFile/helloworld.sh"
           cmd=["/bin/sh",runfile]                #子进程将要执行的命令
           exitValue=call(cmd)                    #创建子进程，结束后，把返回值赋给  exitValue       
           if exitValue!=0:           
           	   req.write("""<h2>Error to excute!</h2><br></body></html>""")
           else:                      
           	   req.write("""<h2>Success to excute!</h2><br>""")
      except Exception,e:
      	   req.write("""Error!""")
      finally:
           req.write("""<h2>Finish!</h2></body></html>""")
      return apache.OK


