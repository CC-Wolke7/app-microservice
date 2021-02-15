FROM nginx:1.15.8

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./static /srv/www/static

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
