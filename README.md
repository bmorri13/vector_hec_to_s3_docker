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
- `vector/hec_to_s3.yaml`
    - **NOTE**: replace the `bucket` value with the name of your bucket before building the container.

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
docker run \
  -p 8088:8088\
  -e VECTOR_ACCESS_KEY_ID='REDACTED'\
  -e VECTOR_SECRET_ACCESS_KEY='REDACTED'\
  vector_hec_to_s3
```

## Data Partitioning
For this example, we will be implementing the paritioning granularity to be down to the year and date format with the S3 key prfix below
```
bronze/{{ splunk_sourcetype }}/partitioned/year=%Y/month=%m/day=%d/
```
- This will have your data land into a bronze data tier with your sourcetype name that was sent to HEC and be included in the partitioned directory.
    - Depending on your use case(s), you may need to adjust this accordingly to change your partitioned accordingly (ie.) make it more granular to hour / minute or even reduce the structure to be simpler.

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
docker run -p 8088:8088 -e VECTOR_ACCESS_KEY_ID='REDACTED' -e VECTOR_SECRET_ACCESS_KEY='REDACTED' -it --entrypoint /bin/sh vector_hec_to_s3

## Once in the container
vector --verbose
```
