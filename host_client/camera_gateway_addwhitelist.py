import cv2,socket,struct,pickle,json,time

SERVER_IP="127.0.0.1";PORT=9100
ANGLES=[("front","Face camera"),("left","Turn left 30°"),
        ("right","Turn right 30°"),("down","Look down slightly"),
        ("up","Look up slightly")]

def main():
    cap=cv2.VideoCapture(0)
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((SERVER_IP,PORT))
    name=input("Enter new person name: ").strip() or "new_person"

    for tag,tip in ANGLES:
        print(f"\n{tag}: {tip}")
        while True:
            r,f=cap.read()
            if not r:continue
            cv2.putText(f,tip,(40,60),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,0),2)
            cv2.imshow("Register",f)
            k=cv2.waitKey(1)&0xFF
            if k==13:
                _,buf=cv2.imencode(".jpg",f)
                info=json.dumps({"name":name,"angle":tag}).encode()
                client.sendall(struct.pack("Q",len(info))+info)
                data=pickle.dumps(buf,protocol=pickle.HIGHEST_PROTOCOL)
                client.sendall(struct.pack("Q",len(data))+data)
                hdr=client.recv(8)
                sz=struct.unpack("Q",hdr)[0]
                msg=json.loads(client.recv(sz).decode())
                print(msg["message"]);break
            elif k==27:break

    cap.release();client.close();cv2.destroyAllWindows()
    print("Registration finished.")

if __name__=="__main__":
    main()