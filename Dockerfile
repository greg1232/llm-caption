###############################################################################
# CPU BASE IMAGE
FROM ubuntu:24.04 AS cpu

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update -y \
    && apt-get install -y python3 python3-pip python3-venv rsync ffmpeg

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python3 -m venv $VIRTUAL_ENV
RUN . $VIRTUAL_ENV/bin/activate

RUN pip install uv

ARG INSTALL_ROOT=/app/llm_caption
###############################################################################

###############################################################################
# LLM_CAPTION PLATFORM IMAGE
FROM cpu AS llm_caption

COPY ./requirements.txt ${INSTALL_ROOT}/requirements.txt

RUN uv pip install --no-compile --no-cache-dir -r ${INSTALL_ROOT}/requirements.txt

WORKDIR ${INSTALL_ROOT}

ENV PYTHONPATH="${PYTHONPATH}:${INSTALL_ROOT}/infra"

COPY ./cmd ${INSTALL_ROOT}/cmd
COPY ./infra ${INSTALL_ROOT}/infra
COPY ./scripts ${INSTALL_ROOT}/scripts
COPY ./Dockerfile ${INSTALL_ROOT}/Dockerfile
COPY ./README.md ${INSTALL_ROOT}/README.md
COPY ./llm_caption ${INSTALL_ROOT}/llm_caption
###############################################################################
