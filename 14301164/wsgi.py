#coding=gbk
import socket
import time
  
  
class wsgi(object):
  
    def __init__(self, HOST, PORT):
         
        #����һ��socket(��ַ��ʽ��tcpЭ��)
        self.asocket = asocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         
        #����socket����
        asocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
         
        #�󶨴������ĵ�ַ
        asocket.bind((HOST, PORT))
         
        #�������Ӹ���
        asocket.listen(20)
         
        #�õ�������ַ�Ͷ˿ں�
        host, port = self.asocket.getsockname()[:2]
         
        #ͨ��������������������������ö˿ں�
        self.server_name = socket.getfqdn(host)
        self.server_port = port
    
    def set_app(self, application):
        self.application = application
        
    def serve_forever(self):
         
        #������ǰϵͳ
        socket = self.asocket
        while True:
            try:
                #�õ��û�������
                self.client_connection, client_address = socket.accept()
                        
                #����һ���û�����в���
                self.arequest()
            except:
                self.asocket.close() 
                httpd = make_server('', 8888, None)
                httpd.serve_forever()
  
    def arequest(self):
        #�õ�������Ϣ        
        self.data = data = self.client_connection.recv(1024)[:]

        #��������ͷ��Ϣ,���������ֵ� 
        env = self.deal_data(data)
  
        #���ú��������践��ֵ
        try:
            response = self.application(env, self.start_response)
        except:
            self.start_response('200 OK', [('Content-type', 'text/html')])
            response = self.get_response()
        
        
        #���Э��ͷ�����ݴ���
        self.finish_response(response)
        
    def get_response(self):
        
        #���ݲ�ͬ״̬������ͬ����ֵ 
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
         
        #�ֽ��ַ�����ɾ���ֽ��Ļ��з�
        request_line = data.splitlines()[0][:]
         
        #�����ݲ��Ϊ��������
        (self.request_method, self.path,self.request_version) = request_line.split()
        
        env = {}
        #���������Դ��������ֵ�
        env['REQUEST_METHOD']    = self.request_method
        env['PATH_INFO']         = self.path
        env['SERVER_NAME']       = self.server_name
        env['SERVER_PORT']       = self.server_port
        return env
  
    def start_response(self, status, headers, exc_info=None):
        
        self.status = status
        nowtime = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.localtime())
        #�������ͷ����
        headers2 = [('Date', nowtime)]
        self.headers = headers2 + headers
    
    def finish_response(self, response):
        try:
            #����������ݣ��γ����ķ���ֵ
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
    #����wsgi���
    server = wsgi(HOST, PORT)
    server.set_app(application)
    return server
  
  
if __name__ == '__main__':
    
    #����server����
    httpd = make_server('', 8888, None)
    httpd.serve_forever()