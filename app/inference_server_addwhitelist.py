import socket, struct, pickle, json, numpy as np, cv2, insightface
from add_whitelist_database import save_whitelist_entry

PORT=9100
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("0.0.0.0",PORT)); server.listen(1)
print("Add-whitelist server ready on 9100")
conn,_=server.accept()

app=insightface.app.FaceAnalysis(allowed_modules=['detection','recognition'])
app.prepare(ctx_id=-1)

stored_embeddings={}
while True:
    h1=conn.recv(8)
    if not h1:break
    size1=struct.unpack("Q",h1)[0]
    info=json.loads(conn.recv(size1).decode())
    name,angle=info["name"],info["angle"]

    h2=conn.recv(8); size2=struct.unpack("Q",h2)[0]
    data=b""
    while len(data)<size2:
        data+=conn.recv(size2-len(data))
    jpg=pickle.loads(data)
    frame=cv2.imdecode(np.frombuffer(jpg,np.uint8),cv2.IMREAD_COLOR)

    faces=app.get(frame)
    if faces:
        emb=faces[0].embedding
        stored_embeddings.setdefault(name,[]).append(emb)
        msg=f"{angle} captured"
    else:
        msg=f"No face found ({angle})"

    res=json.dumps({"message":msg}).encode()
    conn.sendall(struct.pack("Q",len(res))+res)

for n,e in stored_embeddings.items():
    save_whitelist_entry(n,np.array(e))
print("Whitelist updated.")