FROM node:14.15-alpine as node

RUN mkdir -p /src
WORKDIR /src

RUN apk update && \
    apk upgrade && \
    apk add curl python make g++
RUN yarn install

ENV TZ Asia/Tokyo
ENV HOST 0.0.0.0
EXPOSE 3000
