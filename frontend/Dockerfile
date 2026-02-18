# Serve a small static frontend with nginx
FROM nginx:alpine
# Remove default nginx content and copy our dist
RUN rm -rf /usr/share/nginx/html/*
COPY dist /usr/share/nginx/html
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
