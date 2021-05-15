described_pod = b"""Name:         pod_name-hash
Namespace:    namespace
Priority:     0
Node:         node/127.0.0.1
Start Time:   Fri, 14 May 2021 12:49:27 +0200
Labels:       name=pod_name
cni.projectcalico.org/podIP: 127.0.0.1/32
Status:       Running
IP:           127.0.0.0
IPs:
IP:           127.0.0.0
Controlled By:  Controller
Containers:
app:
Container ID:  docker://id_hash
Image:         aa.aa.io/project_name:c8f76d8f4e1b361ddcaf6086f70d9bb5e44487ab
Image ID:      docker://aa.aa.io/project_name@sha256:d2034d8c7076124ce92d9779ab610498b9f58dcec0d895103cc0e8c79907f83d
Port:          <none>
Host Port:     <none>
Command:
celery
Args:
./main.py
State:          Running
Started:      Fri, 14 May 2021 12:49:36 +0200
Ready:          True
Restart Count:  0
Limits:
cpu:     100m
memory:  100M
Requests:
cpu:     100m
memory:  100M
Liveness:  exec [sh -c echo ""]
Environment:
Conditions:
Type              Status
Initialized       True
Ready             True
ContainersReady   True
PodScheduled      True
Volumes:
default-token:
Type:        Type
SecretName:  token
Optional:    false
Events:          <none>
"""
