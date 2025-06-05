# INSIDER

Welcome to the INSIDER!

INSIDER is a tool for designing and deploying edge cloud applications. It is a web-based tool that allows users to design edge cloud applications using a graphical user interface.

The application built with AngularJS and Bootstrap for the UI, jQuery for DOM utilities, and a Python backend (Django) that integrates with OpenAI’s API for intelligent service matching. Docker ensures easy deployment and reproducibility.

## Installation

### Prerequisites

The following software must be installed on your system:

-   Docker (https://docs.docker.com/get-docker/)
-   Git and Github CLI

The rest of the dependencies will be installed automatically when running the `docker-compose.yml` file.

### Installation Steps

1. **Clone this repository**:

    ```bash
    git clone https://github.com/SCAlabUnical/INSIDER.git
    ```
2. **Add the OpenAI API key**:

    Inside the `INSIDER/ecc-workflow-api-server/Dockerfile.dev` file substitute this
    ```bash
    ENV GPT_KEY <OpenAI_API_KEY>
    ```
    with your own OPENAI API key
3. **Build the Docker images**:

    Navigate to the cloned repository directory and run the following command to build the Docker images:

    ```bash
    docker compose build --progress=plain
    ```

    **NOTE**: the `--progress=plain` flag is used to show the build progress in plain text format, which can be helpful for debugging purposes.

4. **Start the Docker containers**:
   After the build is complete, you can start the Docker containers by running:

    ```bash
    docker compose up
    ```

    This will start the INSIDER application and its dependencies.

    **NOTE**: the `-d` or `--detach` flag is not advised because all the logs will be sent to the background and you won't be able to see them.

5. **Access the INSIDER application**:
   Open your web browser and navigate to `http://localhost:3000`. This will take you to the INSIDER application interface.


You can find the complete documentation [here](https://github.com/SCAlabUnical/INSIDER/wiki).

## References
- L. Belcastro, F. Marozzo, A. Presta, R. Varchera, A. Vinci, "Developing Platform-Agnostic IIoT Applications in Edge-Cloud Environments". 7 International Conference on Industry 4.0 & Smart Manufacturing 2024 (ISM 2024), vol. 253, pp. 2106-2115, 2025.
- L. Belcastro, C. Cosentino, F. Marozzo, A. Presta, P. Trunfio, "Empowering Efficient Drone Monitoring with Low-Latency Edge-Cloud Continuum Platforms". 33rd Euromicro International Conference on Parallel, Distributed, and Network-Based Processing (PDP 2025), 2025.
- F. Marozzo, A. Presta, R. Varchera, A. Vinci, "Estimating performances of Application Deployment on Distributed IoT-Edge-Cloud Infrastructures". 22nd IEEE International Conference on Pervasive Intelligence and Computing (PICom 2024), pp. 156-161, 2024.
- L. Belcastro, F. Marozzo, A. Orsino, A. Presta, A. Vinci, "Developing Cross-Platform and Fast-Responsive Applications on the Edge-Cloud Continuum". 15th IFIP Wireless and Mobile Networking Conference (WMNC 2024), pp. 589-594, 2024
