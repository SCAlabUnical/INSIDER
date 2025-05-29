# Edge Cloud Continuum Designer (ECCD)

## Table of Contents

-   [Introduction](#introduction)
-   [Installation](#installation)
    -   [Prerequisites](#prerequisites)
    -   [Installation Steps](#installation-steps)

## Introduction

ECCD is a tool for designing and deploying edge cloud applications. It is a web-based tool that allows users to design edge cloud applications using a graphical user interface.

## Installation

### Prerequisites

The following software must be installed on your system:

-   Docker (https://docs.docker.com/get-docker/)
-   Git and Github CLI\*

The rest of the dependencies will be installed automatically when running the `docker-compose.yml` file.

### Installation Steps

1. **Clone this repository**:

    ```bash
    git clone https://github.com/AleandroPresta/eccd-init.git
    ```

2. **Build the Docker images**:

    Navigate to the cloned repository directory and run the following command to build the Docker images:

    ```bash
    docker compose build --progress=plain
    ```

    **NOTE**: the `--progress=plain` flag is used to show the build progress in plain text format, which can be helpful for debugging purposes.

3. **Start the Docker containers**:
   After the build is complete, you can start the Docker containers by running:

    ```bash
    docker compose up
    ```

    This will start the ECCD application and its dependencies.

    **NOTE**: the `-d` or `--detach` flag is not advised because all the logs will be sent to the background and you won't be able to see them.

4. **Access the ECCD application**:
   Open your web browser and navigate to `http://localhost:3000`. This will take you to the ECCD application interface.
