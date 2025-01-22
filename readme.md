# Depression and Suicide Prediction

## Overview

This project aims to develop a predictive model for identifying individuals at risk of depression and suicide. By leveraging machine learning techniques, the system analyzes various data inputs to provide early warnings, facilitating timely interventions.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Models](#models)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/ravipriy/depression-suicide-prediction.git
   cd depression-suicide-prediction
   ```

2. **Create a Virtual Environment** (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Download Pre-trained Models**:

   Download the necessary models from [this Google Drive link](https://drive.google.com/drive/folders/1Kdez_wbVFBh_CluPQd1AmEeE-E5Bceu7?usp=sharing) and extract all files into the project's root directory.

## Usage

1. **Run the Application**:

   ```bash
   python app.py
   ```

2. **Access the Web Interface**:

   Open your browser and navigate to `http://localhost:5000` to interact with the application.

## Project Structure

```
depression-suicide-prediction/
├── __pycache__/
├── dialogpt_tokenizer/
├── static/
├── templates/
├── advPrediction.py
├── app.py
├── database.py
├── requirements.txt
├── readme.md
└── Project Directory.png
```

- `app.py`: Main application script.
- `advPrediction.py`: Contains advanced prediction algorithms.
- `database.py`: Manages database interactions.
- `static/`: Contains static files (CSS, JavaScript, images).
- `templates/`: HTML templates for the web interface.
- `dialogpt_tokenizer/`: Tokenizer for processing input data.
- `__pycache__/`: Compiled Python files.

## Models

The project utilizes pre-trained models for prediction. Ensure that the models are correctly placed in the root directory as specified in the [Installation](#installation) section.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure that your code adheres to the project's coding standards and includes appropriate tests.
---

*Happy coding!* 
