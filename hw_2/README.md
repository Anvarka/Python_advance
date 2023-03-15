На основе Dockerfile успешно собран:

`docker build -t mydocker -t mydocker .`

Характеристики следующие:

`mydocker  latest    c33c61b33fde   48 minutes ago   78.1MB`

После был запущен(чтобы забрать оттуда, нужно запустить):

`docker run -t -i c33c61b33fde`
 
В artifacts был нужный нам pdf, скопировал его из докера так:

`docker cp mydocker:/artifacts/latex.pdf .`