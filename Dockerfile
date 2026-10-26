# Ubuntu 24.04/Python development image with pdf2htmlEX and its native libs.
# Pin the digest so deployments never pick up an unreviewed mutable image tag.
FROM wayoyo/python-pdf2htmlex@sha256:a9f2ea87e5d7a2750652e09ae1b52a27c65f7140be2ddd5cb72ce17aeed568d1

USER root
WORKDIR /app

# Isolate the application from packages preinstalled by the base image.
RUN python3 -m venv /opt/app-venv
ENV PATH="/opt/app-venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1

COPY Pipfile Pipfile.lock ./
RUN python -m pip install --no-cache-dir --upgrade "pip>=26.2.2,<27" "pipenv==2026.10.3" && \
    pipenv verify && \
    pipenv sync --system && \
    python -m pip uninstall -y pipenv

COPY . .
RUN python -c "import certifi, flask, lxml, PIL, requests; print('certifi:', certifi.__version__)" && \
    command -v pdf2htmlEX

EXPOSE 5000
ENTRYPOINT []
CMD ["python", "run.py"]
