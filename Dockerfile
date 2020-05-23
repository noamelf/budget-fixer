FROM frolvlad/alpine-miniconda3

RUN apk --update add git less openssh && \
    rm -rf /var/lib/apt/lists/* && \
    rm /var/cache/apk/*

WORKDIR /app

# Create the environment:
COPY environment.yaml .env ./
RUN conda env create -f environment.yaml \
    && conda clean -afy

COPY toshl_fixer toshl_fixer

CMD conda run -n toshl-fixer gunicorn --bind :${PORT-8080} --workers 1 --threads 8 toshl_fixer.app:app
