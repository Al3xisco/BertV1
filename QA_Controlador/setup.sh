version=`date "+%H-%M-%S_%d-%m-%y"`
echo $version

docker build -t qa-api .
docker tag qa-api qa-api-version


# docker run -p 85:8080 -e es_ip='192.168.31.66' -e es_port=9200 qa-api
# docker run -p 86:8080 -e es_ip='localhost' -e es_port=9200 qa-api
