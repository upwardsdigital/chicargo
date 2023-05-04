FROM nginx:latest
RUN apt-get update && apt-get install -y procps
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
RUN mkdir -p /app/src/static
RUN chmod -R 755 /app/src/static
