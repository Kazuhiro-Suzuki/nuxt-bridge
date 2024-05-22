FROM node:20.13-alpine3.18 as node

RUN mkdir -p /src
WORKDIR /src

RUN apk update && \
    apk upgrade && \
    apk add curl python3 make g++
RUN yarn install

ENV TZ Asia/Tokyo
ENV HOST 0.0.0.0
EXPOSE 3000
