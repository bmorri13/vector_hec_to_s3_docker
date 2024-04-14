# Vector Docker Deployment

This guide provides instructions on how to build and run a Vector instance in Docker, which is configured to listen on Splunk HEC and output logs to an AWS S3 bucket.

## Prerequisites

Before you begin, ensure you have the following:

- Docker installed on your machine.
- AWS credentials with access to an S3 bucket.
- A valid Splunk HEC token.

## Files

Ensure that your working directory contains the following files:

- `Dockerfile`
- `vector/hec_to_s3.yaml` - Vector configuration file.

## Building the Docker Image

1. **Create the Dockerfile**: Make sure the Dockerfile is set up as described below:

    ```Dockerfile
    # Use the official Vector image as the base image
    FROM timberio/vector:latest-alpine

    # Copy the Vector configuration file into the container
    COPY vector/hec_to_s3.yaml /etc/vector/hec_to_s3.yaml

    # Expose the port Vector is configured to listen on
    EXPOSE 8088

    # Command to run Vector
    ENTRYPOINT ["vector", "--verbose", "--config", "/etc/vector/hec_to_s3.yaml"]
    ```

2. **Build the Docker image** with the following command:

    ```bash
    docker build -t vector_hec_to_s3 .
    ```

## Running the Docker Container

Run the Docker container using the following command. Replace `your-access-key-id` and `your-secret-access-key` with your actual AWS credentials.

```bash
docker run
  -p 8088:8088\
  -e S3_BUCKET_NAME='<REPLACE ME>'\
  -e VECTOR_ACCESS_KEY_ID='REDACTED'\
  -e VECTOR_SECRET_ACCESS_KEY='REDACTED'\
  vector_hec_to_s3
```

## Testing HEC to S3 Logic
### Files

To run a simple test locally, utlize the following file (NOTE: This is assuming you have python installed on your local machine or by other means)

- `scripts/random_hec_log_generator.py` - Sample python log generator file

```bash
python random_hec_log_generator.py
```


## Troubleshooting
### To run the Docker Container for troubleshooting
```bash
docker run -p 8088:8088 -e S3_BUCKET_NAME='<REPLACE ME>' -e VECTOR_ACCESS_KEY_ID='REDACTED' -e VECTOR_SECRET_ACCESS_KEY='REDACTED' -it --entrypoint /bin/sh vector_hec_to_s3

## Once in the container
vector --verbose
```