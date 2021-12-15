# build env
FROM node:13.12.0-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . ./
RUN npm run build
COPY ./docs/redoc.html result_build/redoc/api/docs/redoc.html
COPY ./docs/openapi-schema.yml result_build/redoc/api/docs/openapi-schema.yml
RUN cp -r build result_build
RUN mv result_build/build/static/ .