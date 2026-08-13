FROM node:24-slim AS build

WORKDIR /app

# Copy dependency files first to use Docker cache
COPY package*.json ./
RUN npm install

# Copy code and run the static build
COPY . .
RUN npm run build

FROM node:24-slim
WORKDIR /app

COPY --from=build /app/build ./build
COPY package*.json ./
RUN npm ci --omit=dev

EXPOSE 3000
ENV PORT=3000
CMD ["node", "build"]