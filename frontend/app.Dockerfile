ARG NODE_VERSION=24.18

# Build stage
FROM mirror.gcr.io/node:${NODE_VERSION}-alpine AS build-stage
WORKDIR /app

ARG NPM_REGISTRY
ARG NPM_SCOPE
ARG NPM_TOKEN

COPY package*.json ./
RUN set -eu; \
  if [ -n "${NPM_TOKEN:-}" ] || [ -n "${NPM_REGISTRY:-}" ] || [ -n "${NPM_SCOPE:-}" ]; then \
    if [ -z "${NPM_TOKEN:-}" ] || [ -z "${NPM_REGISTRY:-}" ] || [ -z "${NPM_SCOPE:-}" ]; then \
      echo "NPM_TOKEN, NPM_REGISTRY, and NPM_SCOPE must be provided together."; \
      exit 1; \
    fi; \
    REG="${NPM_REGISTRY}"; \
    case "$REG" in */) ;; *) REG="${REG}/" ;; esac; \
    HOST="${REG#https://}"; \
    HOST="${HOST#http://}"; \
    printf "%s:registry=%s\n//%s:_authToken=%s\n" "$NPM_SCOPE" "$REG" "$HOST" "$NPM_TOKEN" > .npmrc; \
  fi; \
  npm ci --include=dev --ignore-scripts; \
  rm -f .npmrc

COPY . .

ARG VITE_API_BASE_URL
ARG VITE_BASE_PATH=/
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}
ENV VITE_BASE_PATH=${VITE_BASE_PATH}
ENV NODE_ENV=production
ENV MODE=production

RUN npm run build

# Production stage
FROM mirror.gcr.io/node:${NODE_VERSION}-alpine AS production-stage
WORKDIR /app

ENV NODE_ENV=production

RUN npm install -g serve@14
COPY --from=build-stage /app/dist ./dist

EXPOSE 80

CMD ["serve", "-s", "dist", "-l", "80"]
