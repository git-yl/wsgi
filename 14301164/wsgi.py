#coding=gbk
import socket
import time
  
  
class wsgi(object):
  
    def __init__(self, HOST, PORT):
         
        #建立一个socket(地址格式，tcp协议)
        self.asocket = asocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         
        #设置socket属性
        asocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
         
        #绑定传过来的地址
        asocket.bind((HOST, PORT))
         
        #设置连接个数
        asocket.listen(20)
         
        #得到主机地址和端口号
        host, port = self.asocket.getsockname()[:2]
         
        #通过主机名返回完整主机名，获得端口号
        self.server_name = socket.getfqdn(host)
        self.server_port = port
    
    def set_app(self, application):
        self.application = application
        
    def serve_forever(self):
         
        #监听当前系统
        socket = self.asocket
        while True:
            try:
                #得到用户的连接
                self.client_connection, client_address = socket.accept()
                        
                #连接一个用户后进行操作
                self.arequest()
            except:
                self.asocket.close() 
                httpd = make_server('', 8888, None)
                httpd.serve_forever()
  
    def arequest(self):
        #得到需求信息        
        self.data = data = self.client_connection.recv(1024)[:]

        #处理需求头信息,返回数据字典 
        env = self.deal_data(data)
  
        #调用函数，给予返回值
        try:
            response = self.application(env, self.start_response)
        except:
            self.start_response('200 OK', [('Content-type', 'text/html')])
            response = self.get_response()
        
        
        #结合协议头将数据传回
        self.finish_response(response)
        
    def get_response(self):
        
        #根据不同状态给出不同返回值 
        path1 = self.path[1:]
        path2 = self.path
        if path2[-5:] == '.html' :
            try:
                response = open(path1).read( )
            except:
                self.status = '404 Not Found'
                response = '404 Not Found'
                
        elif path2[-4:] == '.htm' :
            try:
                response = open(path1).read( )
            except:
                self.status = '404 Not Found'
                response = '404 Not Found'
        else :
            response = 'hello ' + path1
        return response
  
    def deal_data(self, data):
         
        #分解字符串，删除分解后的换行符
        request_line = data.splitlines()[0][:]
         
        #将数据拆分为具体属性
        (self.request_method, self.path,self.request_version) = request_line.split()
        
        env = {}
        #将部分属性存入数据字典
        env['REQUEST_METHOD']    = self.request_method
        env['PATH_INFO']         = self.path
        env['SERVER_NAME']       = self.server_name
        env['SERVER_PORT']       = self.server_port
        return env
  
    def start_response(self, status, headers, exc_info=None):
        
        self.status = status
        nowtime = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.localtime())
        #添加其他头数据
        headers2 = [('Date', nowtime)]
        self.headers = headers2 + headers
    
    def finish_response(self, response):
        try:
            #添加其他数据，形成最后的返回值
            headers = self.headers
            status = self.status
            response2 = 'HTTP/1.1 {status}\r\n'.format(status=status)
            for header in headers:
                response2 += '{0}: {1}\r\n'.format(*header)
            response2 += 'Server: WSGIServer 0.2\r\n\r\n'
            for data in response:
                response2 += data
            self.client_connection.sendall(response2)
        finally:
            self.client_connection.close()
            
  
def make_server(HOST, PORT, application):
    #调用wsgi框架
    server = wsgi(HOST, PORT)
    server.set_app(application)
    return server
  
  
if __name__ == '__main__':
    
    #创建server服务
    httpd = make_server('', 8888, None)
    httpd.serve_forever()