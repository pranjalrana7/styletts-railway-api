FROM jrottenberg/ffmpeg:6.0-alpine
WORKDIR /app
COPY server.js .
COPY package*.json .
RUN npm install
CMD ["node", "server.js"]
