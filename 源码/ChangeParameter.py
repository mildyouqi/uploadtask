from mod_python import apache,util,Session
import os
def handler(req,sess):
      basePath="/home/youqi/Desktop/cg-rtl/testcase/"
      form = util.FieldStorage(req)    
      v_version=form["version"].value  
      v_platform=form["platform"].value
      v_testcase=form["testcase"].value
      filePath=basePath + v_testcase + "/" 
      if not os.path.exists(basePath):  
      	    os.mkdir(basePath)
      req.content_type="text/html"
      req.write("""<html><head><title>change parameter</title></head>
               <body>change parameter successfully!</body></html>""")
      sess["version"]=v_version          
      sess["platform"]=v_platform        
      sess["testcase"]=filePath
      sess.save()
      return apache.OK
