# Use the official Vector image as the base image
FROM timberio/vector:latest-alpine

# Copy the Vector configuration file into the container
COPY vector/hec_to_s3.yaml /etc/vector/hec_to_s3.yaml

# Expose the port Vector is configured to listen on
EXPOSE 8088

# Command to run Vector
ENTRYPOINT ["vector", "--verbose", "--config", "/etc/vector/hec_to_s3.yaml"]
