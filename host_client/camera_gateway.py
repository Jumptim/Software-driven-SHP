import cv2, socket, struct, pickle, json, time, numpy as np

SERVER_IP="127.0.0.1"; PORT=9000
MATLAB_IP="127.0.0.1"; MATLAB_PORT=5005
SEND_INTERVAL = 0.05

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cap=cv2.VideoCapture(0)
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((SERVER_IP,PORT))

last_send_time=0

while True:
    ret,frame=cap.read()
    if not ret:continue

    _,buf=cv2.imencode(".jpg",frame)
    data=pickle.dumps(buf,protocol=pickle.HIGHEST_PROTOCOL)
    client.sendall(struct.pack("Q",len(data))+data)

    hdr=client.recv(8)
    if not hdr:break
    size=struct.unpack("Q",hdr)[0]
    payload=b""
    while len(payload)<size:
        payload+=client.recv(size-len(payload))
    res=json.loads(payload.decode())

    # Draw boxes
    for b in res["boxes"]:
        x1,y1,x2,y2,color=b
        cv2.rectangle(frame,(x1,y1),(x2,y2),color,2)
    if res["text"]:
        cv2.putText(frame,res["text"],(60,100),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),4)
    if res.get("name"):
        cv2.putText(frame,res["name"],(60,160),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)

    # Send UDP to MATLAB with console feedback
    now = time.time()
    if now - last_send_time > SEND_INTERVAL:
        button = res.get("button", 0)
        udp_sock.sendto(np.array([button], dtype=np.uint8).tobytes(),
                        (MATLAB_IP, MATLAB_PORT))
        state = "Sent button=1 (Face+FingerUp)" if button == 1 else "Sent button=0"
        print(f"[{time.strftime('%H:%M:%S')}] {state}")
        last_send_time = now

    cv2.imshow("Real-Time Recognition",frame)
    if cv2.waitKey(1)&0xFF==27:break

cap.release();client.close();udp_sock.close();cv2.destroyAllWindows()