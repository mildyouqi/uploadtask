from mod_python import apache,util,Session
from subprocess import call
def handler(req,sess):
      v_version=sess["version"]    
      v_platform=sess["platform"]
      v_testcase=sess["testcase"]
      runfile = "/home/youqi/Desktop/ExcuteFile/helloworld.sh"   
      req.content_type='text/html'
      req.write("""<html><head><title>JSP TestCase</title></head><body>""")
      try:
      	  cmd=["/bin/sh",runfile]    
          exitValue=call(cmd)       
          req.write(runfile)        
          req.write("""<br>""")
          if exitValue !=0:          
          	  req.write("""<h2>Error to excute!</h2><br>""")
          else:                      
          	  req.write("""<h2>Success to excute!</h2><br>""")
      except Exception,e:
      	  req.write("""Error!""")
      finally:
      	  req.write("""<h2>Finish!</h2>
      	  	</body>
      	  	</html>""")
      return apache.OK
