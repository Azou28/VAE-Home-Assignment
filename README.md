## Setup Instructions 
### 1. Clone repo

    git clone https://github.com/Azou28/VAE-Home-Assignment.git
    cd VAE-Home-Assignment

### 2. Create virtual environment (Recommended)

    python3 -m venv .venv
    source .venv/bin/activate

### 3. Install Robot Framework

    pip install robotframework

## Assumptions
    - **Python 3.10+**
    - Tests are executed locally (Windows/Linux/macOS).
    - The “API” is an **in-process Python API** (Robot calls Python keywords / libraries).
    - UUID/serial generation is a mock script with internal logic - not following any protocol

## Run Commands
    - To run robot tests and save in the results folder
    ```
        cd <repo_root>
        robot -d robot/results  robot/Robot_Tests.robot
    ```
    - Results will be save in ./robot/results

