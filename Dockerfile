FROM node:20-alpine

# Install FFmpeg
RUN apk add --no-cache ffmpeg

WORKDIR /app

# Copy package.json first
COPY package*.json ./

# Update npm and install dependencies
RUN npm install -g npm@11.6.4
RUN npm install

# Copy the rest of the code
COPY server.js .

CMD ["node", "server.js"]
