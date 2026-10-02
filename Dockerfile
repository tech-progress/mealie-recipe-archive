FROM ghcr.io/mealie-recipes/mealie:v3.28.0@sha256:8b02290f4d1806f02acac6f25f6d48a3c965612fda1f8e914d5af533276f8688
COPY --chmod=755 entrypoint.sh /template-entrypoint.sh
COPY bootstrap.py /template-bootstrap.py
COPY template_app.py /app/template_app.py
ENTRYPOINT ["/template-entrypoint.sh"]
