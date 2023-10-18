## Step 1

第一步先打包專案
docker build . -t <image_name>
(使用docker-compose須將dockerfile中的CMD註解)

## Step 2
  ### docker compose
  使用docker compose方法時 需先執行 
  docker network create puyuan_net --subnet 172.21.0.0/24
  建立虛擬網卡以便固定容器的ipv4
  須將docker-compose.yml的puyuan_main的image改為你build時的<image_name>
  
  ### docker run
  使用docker run方法時 需開啟本地的資料庫ex: mysql, mariadb
  再執行
  docker run -itd --name <container_name> --network=bridge -p 8000:8000 <image_name>

## Step 3
  修改puyuan_case/settings.py中的資料庫設定
  ```
  vi puyuan_case/settings.py
  
  :94 (第94行的意思)
  
  HOST: "<本機ipv4>" (改ip) # docker run
  HOST: "<mariadb ipv4>" (改ip) # docker compose
  ```

## 註
 請注意!! 在./puyuan_case/settings.py的87行開始的設定,有分docker-compose版與docker run&local版
 請注意!! 不管是docker run或docker-compose方法,在docker build前再次確認./Dockerfile的CMD部分