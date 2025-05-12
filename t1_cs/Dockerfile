# use a base python image
FROM python:3.11-slim

# set the working directory inside the container
WORKDIR /app

# copy the app code to the container
COPY . /app

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# expose the port fastapi will run on
EXPOSE 8000

# command to run the server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]