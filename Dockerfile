FROM python

COPY . /taxi-data-analysis/

RUN pip install -r /taxi-data-analysis/requirements.txt  && \
    pip install --upgrade /taxi-data-analysis


WORKDIR /taxi-data-analysis

ENV TINI_VERSION v0.14.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

ENTRYPOINT ["/tini", "--","processing"]
