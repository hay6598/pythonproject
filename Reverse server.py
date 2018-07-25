import socket    #서버 파일을 생성후 socket, sys 모듈을 불러온다
import sys

#소켓 생성
def socket_create(): #socket_create() 함수를 정의한다.   
    try:
        global host     #try를 사용해서 host, port, s 변수를  global로 설정
        global port
        global s
        host = '203.230.91.250'      #호스트 주소를 입력하고
        port = 9999                  #임의로 값을 넣어준다.
        s = socket.socket()
    except socket.error as msg:      #소켓을 생성하는데 있어서 에러가 발생한다면 그것을 msg라는 변수로 여긴다.
        print("socket creation error: " + str(msg)) #에러가 발생하면 사용자가 알 수 있게 에러발생 메시지를 출력한다.

#통신을 하기 위해서는 통신 기기간 데이터가 어디에서 오고 어디로 가는지 알아야하는데 이럴 때 사용하는 개념이 host와port이다. 이를 바인드 해주어야 어떤 데이터가 오가는지 쉽게 파악할 수 있기 떄문에 소켓 바인딩을 한다.
#소켓 바인딩
def socket_bind(): #소켓바인더 함수를 정의한다.
    try:
        global host #사용할 변수들을 global로 지정한다.
        global port 
        global s
        print("Binding socket to port: " + str(port))  #프린트 라인을 넣어 프리징이 일어나고 있지 않는 것을 확인하게 한다. 그리고 지정한 포트는 임의의 숫자이기 떄문에 출력하기 전에 스트링으로 컨버팅을 해주기 위해 str()을 사용한다.
        s.bind((host, port))  #데이터 바인딩을 하기위해 bind를 호출하여 Tuple의 형태로 호스트, 포트를 넣어줬다.
        s.listen(5)  #포트 듣고 열기위해 listen을 호출하고 여기서 받은5는 이숫자를 넘기면 리버싱 하겠다는 의미이다.( 너무 많은 커넥션을 받아들이면 서버에 로드가 걸릴 수 있기 떄문이다.)
    except socket.error as msg:#소켓 바인딩이 실패하면 소켓 바인딩 에러를 출력한다.
        print("Socket binding error: " + str(msg) + "\n" + "Retrying.....") #다시 바인딩을 시도하게 하기위해 Retrying.. 메시지를 출력한다.
        socket_bind() # socket_bind()를 통해 다시 시도하게 만든다.

def socket_accept(): #소켓 받아들이
    conn, address = s.accept() #listen()이 작동하고 있고 소켓을 받아들이면 새로운 커넥션을 수용한다.
    print("Connection has been established | "+"IP: " + address[0] + " | port" + str(address[1])) #서버에 연결이되면 먼저 아이피주소를 할당하고, 다음은 포트넘버가 할당된다. address는 접속자의 데이터정보를 알려준다.
    send_commands(conn) #conn은 명령을 주고 받을 때 대기하고 있다가 입력을 받으면 실행하고 그 결과를 우리에게 보내준다.
    conn.close() #통신을 주고 받다가 종료를 하면 conn을 닫는다.
    
def send_commands(conn): #명령어를 보내기 위한 함수를 정의한다.
    while True: #명령어를 한번 보내고 그만할것이 아니기때문에 계속 사용하기위해서 반복문을 사용한다.
        cmd = input() #내가 입력할 명령어를 input()으로 넣고 cmd라는 변수에 저장을 한다.
        if cmd == 'quit': #cmd값이 'quit'라는 입력을 받으면 모든 과정을 종료시킨다.
            conn.close()
            s.close()
            sys.exit()  #cmd =='quit'가 만족되면 conn인 커넥션도 종료하고 소켓 s를 종료시키고 sys도 빠져나온다.
        if len(str.encode(cmd)) > 0: #cmd 값에 입력값이 들어오면 010110 (bytes)로 전달해야 하기때문에 encode()를 해준다.
            conn.send(str.encode(cmd)) #encode 된 값을 conn을 통해서 보내주는 평선 send()를 사용한다. 
            client_response = str(conn.recv(2048), "utf-8") #클라이언트에게 보낸 명령어를 클라이언트는 수행하고 그 결과를 conn.recv로 받는다. 그 버퍼 사이즈는 2048로 해준다. 그리고 사람이 읽을 수 있는 값으로 표헌하기 위해서 "utf-8"로 문자화로 바꾸어 client_response변수에 저장한다.
            print(client_response, end="") #명령어를 보내 받은 수행 결과를 내 컴퓨터에서 읽을 수 있도록 프린터 아웃한다.

def main(): #메인 함수를 정의하고 상기의 함수들을 하나씩 호출하여 실행한다.
    socket_create()
    socket_bind()
    socket_accept()

main() #최종적으로 메인 함수를 호출하여 프로그램이 실행되게 한다.
