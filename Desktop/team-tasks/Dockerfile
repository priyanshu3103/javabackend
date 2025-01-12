###################### Stage-1 Build Stage ################################
FROM python:3.9 AS builder
WORKDIR /task
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

 
#################### Stage-2 Final stage ################################
FROM python:3.9-slim

WORKDIR /task

COPY --from=builder /usr/local/lib/python3.9/site-packages/  /usr/local/lib/python3.9/site-packages/

COPY --from=builder /task /task
RUN apt-get update && apt-get install -y libmariadb3
EXPOSE 5000
CMD [ "python","app.py","--host=0.0.0.0" ]

