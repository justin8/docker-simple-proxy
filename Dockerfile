FROM nginx:alpine

RUN apk add --update-cache python3

ADD nginx.conf /etc/nginx/nginx.conf
ADD proxy-config-generator/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
ADD proxy-config-generator /proxy-config-generator

ENTRYPOINT ["python3", "/proxy-config-generator/generate-configs.py", "--start"]
