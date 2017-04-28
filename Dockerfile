FROM nginx:alpine

RUN apk add --update-cache python3

ADD proxy-config-generator /proxy-config-generator
RUN pip3 install -r /proxy-config-generator/requirements.txt

CMD  ["python3", "/proxy-config-generator/generate-configs.py", "--start"]
