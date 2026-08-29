FROM node:22-slim

WORKDIR /app

COPY package*.json ./

RUN npm ci --omit=dev

COPY index.js ./
COPY app.js ./
COPY src ./src

EXPOSE 3000

CMD ["npm", "start"]