from mod_python import apache,util,Session
import os
def handler(req,sess):
      maxFileSize = 5000 * 1024 
      maxMemSize = 5000 * 1024
      v_version=sess["version"] 
      v_platform=sess["platform"]
      filePath=sess["testcase"]
      if not os.path.exists(filePath):
      	    os.mkdir(filePath)
      try:                           
          import msvcrt
          msvcrt.setmode(0,O_BINARY)
          msvcrt.setmode(1,O_BINARY)
      except ImportError:
          pass
      form = util.FieldStorage(req) 
      fileitem=form['file']	        
      fileName=fileitem.filename     
      if fileName.rfind("\\")>=0:  
          fileName=fileName[fileName.rfind("\\"):]
      else:
          fileName=fileName[fileName.rfind("\\")+1:]  
      req.content_type='text/html'
      req.write("""<html><head><title>File upload</title></head><body>""")
      if fileName:
      	  dirname=fileName
      	  fileName=fileName.replace("-", "_")
      	  fileName="V-"+v_version+"P-"+v_platform+"T-"+fileName
      	  sess["dirname"]=dirname
      	  sess.save()
      	  fname=os.path.basename(fileitem.filename)
          fout=open(os.path.join(filePath,fname),'wb')
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

