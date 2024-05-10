# Project Setup Instructions

This README provides instructions on how to set up and run the application. Follow these steps to get started.

## Prerequisites

- Python 3.9.15

## Installation

1. **Install Python 3.9.15**

   Ensure that Python 3.9.15 is installed on your system. You can download it from [Python's official website](https://www.python.org/downloads/).

2. **Install Required Libraries**

   Navigate to the project directory and install the required libraries using pip:

   ``` pip install -r requirements.txt```

3. **Configuration**

To configure the application:

- Open the `config.py` file located in the root directory of your project.
- Modify the settings to include your desired radius for location and the filenames for your Excel sheets. Here is an example of what the `config.py` might look like:

4. **Adding Excel Files**
Place your two Excel files (main_data.xlsx and login_data.xlsx) in the project's root directory. These files should match the names specified in the config.py.

5. **Running the Application**
To run the application, open your terminal or command prompt, navigate to the project directory, and execute the following command:


``` python main.py```