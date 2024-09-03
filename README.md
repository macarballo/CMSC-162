
# Introduction to Image and Video Processing

Welcome to the "Introduction to Image and Video Processing" project repository! This guide will walk you through the setup process for running the project on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- **Python**: Download the latest version from [python.org](https://www.python.org/downloads/).
- **Git**: To clone the repository. You can download it from [git-scm.com](https://git-scm.com/downloads).

## Setup Instructions

Follow these steps to get the project up and running:

### 1. Install Python

- Go to [python.org](https://www.python.org/downloads/).
- Click the **Download Python** button that appears first on the page to download the latest version.
- Follow the installation instructions for your operating system.

### 2. Clone the Repository

Open your terminal or command prompt and run the following command to clone the repository to your local machine:

```bash
git clone <repository-url>
```

Replace `<repository-url>` with the actual URL of your repository.

### 3. Install Dependencies

Navigate to the project directory using your terminal or command prompt, then install the necessary dependencies by running:

```bash
npm install
```

### 4. Activate the Virtual Environment

The virtual environment, `my_venv`, has already been created. To activate it:

1. Open Visual Studio Code.
2. Open the terminal within Visual Studio Code (you can do this by selecting **Terminal** > **New Terminal** from the top menu).
3. Run the following command to activate the virtual environment:

   ```bash
   my_venv\Scripts\activate
   ```

   This will ensure that you’re using the correct Python environment for the project.

### 5. Install Tkinter

Tkinter is required for the graphical user interface. To install Tkinter, run the following command:

```bash
pip install tk
```

## Running the Application

Once everything is set up, you can run the application by executing the main script. In the terminal, navigate to the project directory and run:

```bash
python main.py
```

## Additional Notes

- Make sure to always activate the virtual environment before running the application.
- If you encounter any issues, refer to the project’s documentation or open an issue on the GitHub repository.
