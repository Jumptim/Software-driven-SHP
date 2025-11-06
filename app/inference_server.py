import socket, struct, pickle, json, cv2, numpy as np
from recogfaceyolo_fingeryolo import process_frame

HOST="0.0.0.0"; PORT=9000
srv=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
srv.bind((HOST,PORT)); srv.listen(1)
print("nference server ready on 9000.")
conn,_=srv.accept()

while True:
    header=conn.recv(8)
    if not header: break
    size=struct.unpack("Q",header)[0]
    data=b""
    while len(data)<size:
        data+=conn.recv(size-len(data))
    frame=cv2.imdecode(np.frombuffer(pickle.loads(data),np.uint8),cv2.IMREAD_COLOR)
    result=process_frame(frame)
    payload=json.dumps(result).encode()
    conn.sendall(struct.pack("Q",len(payload))+payload)

conn.close();srv.close()