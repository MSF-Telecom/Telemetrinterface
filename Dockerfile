FROM alpine:3.15.4

# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

# Install npm
RUN apk add --update nodejs
RUN apk add --update npm
RUN npm install node --global
RUN npm install node-dev --global


# Copy files to docker image
ADD ./ControlPanel /ControlPanel
ADD ./python/scripts/Telemetrinterface_STD /Telemetrinterface_STD

# Expose ports
EXPOSE 8080
EXPOSE 8081