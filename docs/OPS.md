# NGINX create password
sudo htpasswd -c ./webhost/nginx/.htpasswd nginx

# Docker
docker-compose -f docker-compose.yml up --build
docker-compose -f docker-compose.yml down -v 