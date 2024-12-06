FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim 
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

COPY . .
RUN /root/.local/bin/uv sync --frozen --no-dev
ENV PATH="/app/.venv/bin:$PATH"
RUN chmod +x start.sh
RUN ./start.sh

LABEL traefik.http.routers.28.entrypoints="websecure"
LABEL traefik.http.routers.28.rule="(Host(`batik.umm.ac.id`) && PathPrefix(`/batik_product/28{regex:$$|/.*}`))"
LABEL traefik.http.routers.28.tls="true"

ENV PORT 5000
EXPOSE 5000
ENV SCRIPT_NAME "/batik_product/28"

WORKDIR /app/web
CMD exec granian --interface wsgi --host 0.0.0.0 --port 5000 --workers 1 --threads 4 web.wsgi:application
