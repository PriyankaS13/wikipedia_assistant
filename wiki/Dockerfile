FROM python:3.8-slim-buster

# Copy all required files
COPY wiki_app.py app.cfg requirements.txt /wiki/

# Changing the working directory to /wiki
WORKDIR /wiki

# install all requirements
RUN pip3 install -r requirements.txt

# Expose the api port
EXPOSE 8000

CMD ["python3", "wiki_app.py"]