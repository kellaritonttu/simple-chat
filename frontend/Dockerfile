FROM node:24-slim

WORKDIR /app

COPY package*.json svelte.config.js ./
RUN npm install --ignore-scripts

COPY . .
RUN npm run build

EXPOSE 3000
CMD ["node", "build"]