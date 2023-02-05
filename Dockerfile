FROM python:3.7

# Expose port you want your app on
EXPOSE 8080

#Optional - install git to fetch packages directly from github
RUN apt-get update && apt-get install -y git

# Copy app code and set working directory
COPY . ~/tatu_re/
WORKDIR ~/tatu_re/


# Upgrade pip and install requirements
RUN pip install -U pip
RUN pip install streamlit plotly pandas
RUN pip install -e .

ENV GOOGLE_ENTRYPOINT="streamlit run dash.py –server.port=8080 –server.address=0.0.0.0"

# Run
ENTRYPOINT ["streamlit", "run", "dash.py", "--server.port=8080", "--server.address=0.0.0.0"]
