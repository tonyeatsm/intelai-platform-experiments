# Doc
```shell
https://inteldevzone.blog.csdn.net/article/details/148951180

```

# Docker pull
```shell

sudo docker pull openvino/ubuntu24_dev:2025.3.0

```


# Docker create
``` shell

sudo docker run -itd \
--restart always \
--name intel-ai-labs_openvino \
--user root \
--device /dev/dri:/dev/dri \
-v /etc/localtime:/etc/localtime \
--ipc=host \
-p 6700:6700 \
-v /data/intel/intel-ai-labs/openvino:/root/openvino \
-w /root/openvino openvino/ubuntu24_dev:2025.3.0


```

# Docker enter  
```shell

sudo docker start intel-ai-labs_openvino
sudo docker exec -it intel-ai-labs_openvino /bin/bash


```



# Docker commit 
```shell

sudo docker commit ranch-brain_manus tonyeatsm/ranch-brain_manus:20251011
sudo docker push tonyeatsm/ranch-brain_manus:20251011



```