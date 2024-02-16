# connect to remote server

On remote device:
```bash
sudo /usr/sbin/ser2net -n -c /etc/ser2net.yaml -P /run/ser2net.pid -l
```
Locally:
```bash
while sleep 1; do echo "Starting..."; socat pty,link=/Users/volodymyrp/dev/_own/m2tech/m2techserial,waitslave,echo=1 tcp:192.168.2.3:1234; done
```


didn't work:
```bash
while sleep 1; do echo "Starting..."; \
socat pty,link=/Users/volodymyrp/dev/_own/m2tech/m2techserial,waitslave,echo=1 \
EXEC:"ssh dreamer@192.168.2.3 socat - /dev/rfcomm/rfcomm0,nonblock,rawer"; done
```

