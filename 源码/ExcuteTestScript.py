from mod_python import apache,util,Session
from subprocess import call
def handler(req,sess):
      v_version=sess["version"]  
      v_platform=sess["platform"]
      v_testcase=sess["testcase"]
      v_filename=sess["dirname"]
      runfile=""
      req.content_type='text/html'
      req.write("""<html><head><title>JSP TestCase</title></head><body><br>""")
      try:
      	   if v_testcase.find("testcase1")!=-1: 
      	   	   runfile = "/home/crdong/main/a.sh"
      	   elif v_testcase.find("testcase2")!=-1:
               dirname=v_filename[:v_filename.index(".tar.gz")] 
               runfile="/usr/local/apache-tomcat-7.0.57/webapps/ROOT/remote.sh"
               util.redirect(req,"http://124.16.141.184:8080/mym_test/"+dirname+"/index_page.html")
           else:                      
               runfile = "/home/youqi/Desktop/ExcuteFile/helloworld.sh"
           cmd=["/bin/sh",runfile]    
           exitValue=call(cmd)        
           if exitValue!=0:           
           	   req.write("""<h2>Error to excute!</h2><br></body></html>""")
           else:                      
           	   req.write("""<h2>Success to excute!</h2><br>""")
      except Exception,e:
      	   req.write("""Error!""")
      finally:
           req.write("""<h2>Finish!</h2></body></html>""")
      return apache.OK
