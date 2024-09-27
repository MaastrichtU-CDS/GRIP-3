# basic python3 image as base
FROM harbor2.vantage6.ai/infrastructure/algorithm-base

# This is a placeholder that should be overloaded by invoking
ARG PKG_NAME="com.grip3.vantage6wrapper"

# install federated algorithm
COPY . /app
RUN pip install /app


# Set environment variable to make name of the package available within the
# docker image.
ENV PKG_NAME=${PKG_NAME}

# Tell docker to execute `wrap_algorithm()` when the image is run. This function
# will ensure that the algorithm method is called properly.
CMD poetry run python -c "from vantage6.algorithm.tools.wrap import wrap_algorithm; wrap_algorithm()"