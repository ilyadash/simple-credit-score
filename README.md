# Проект по прогнозированию кредитного риска

## Обзор

Это проект в области машинного обучения, направленный на прогнозирование кредитных рисков. Система анализирует финансовые данные для предсказания вероятности дефолта взятого частным лицом кредита, что помогает финансовым учреждениям принимать более обоснованные решения при выдаче кредитов.

Использованные данные Kaggle: 
https://www.kaggle.com/datasets/laotse/credit-risk-dataset

Ноутбук, который был взят за основу для выбора модели: 
https://www.kaggle.com/code/anshtanwar/credit-risk-prediction-training-and-eda

## Ключевые особенности

- **Пайплайн обработки данных**: Очистка и предобработка кредитных данных и модель машинного обучения в одном объекте
- **Обучение моделей**: Использование библиотеки scikit-learn для разработки и оценки моделей
- **Готовность к развертыванию**: Бэкенд, готовый к производственному развертыванию с поддержкой Docker
- **Интерактивный фронтенд**: Интерфейс на основе Streamlit для предсказания дефолта по данным

Проект использует ML-пайплайн библиотеки scikit-learn с ансамблем нескольких неглубоких моделей машинного обучения с лучшими метриками:
- Дерево решений (Decision Tree)
- Градиентное бустинговые деревья (CatBoost, LightGBM, Extreme Gradient Boosting)
  
Результаты обученного ансамбля на тестовых данных (20% изначальной выборки):

| Метрика                     | Значение   |
|-----------------------------|------------|
| Общая точность (Accuracy)   | 0.93       |
| Точность (Precision)        | 0.96       |
| Чувствительность (Recall)   | 0.71       |
| Специфичность (Specificity) | 0.99       |
| F1                          | 0.82       |
| Денег дополучено            | 4052211.37 |

## Структура директорий проекта

```
.
├── ml_rnd/                 # Исследования и разработка в области ML
│   ├── src/                # Код для R&D
│   ├── data/               # Хранение наборов данных для обучения моделей
│   └── .env                # Файл с переменными окружения для обработки данных и обучения
├── development/            # Среда разработки
│   ├── backend/            # Сервер API
│   │   └── src/            # Код для окружения разработки
│   │       └── model/      # Обученные модели
│   └── frontend/           # Приложение Streamlit
│       └──  src/           # Код для окружения разработки
└── production/             # Развертывание для продуктового окружения
    ├── backend/            # Сервер API
    │   └── src/            # Код для окружения разработки
    │       ├── main.py     # Приложение FastAPI
    │       ├── db.py       # Операции с базой данных
    │       └── model/      # Обученные модели
    └── frontend/           # Приложение Streamlit
        └──  src/           # Код для продуктового окружения
```

## Используемые технологии

- **Python 3.10+**: Основной язык проекта
- **Scikit-learn**: Основная библиотека машинного обучения для обучения и оценки моделей
- **FastAPI**: Фреймворк бэкенда для предоставления предсказаний
- **Streamlit**: Интерактивный фронтенд для исследования данных
- **Docker**: Контейнеризация для развертывания проекта
- **Pandas/NumPy**: Манипуляция данными и численные вычисления

## Начало работы

### Требования

- Git
- Docker (для контейнерного развертывания)

### Для разработки пайплайна
#### Установка
Рекомендуется использовать Visual Studio Code.
1. Перейдите в папку репозитория:
   ```bash
   cd credit-risk-prediction
   ```

2. Настройте виртуальную среду и установите зависимости:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # На Windows используйте `.venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Перейдите в папку с кодом для R&D
   ```bash
   cd ml_rnd/src
   ```

#### Обучение модели
1. Подготовьте ваш набор данных в формате CSV.
2. Приведите ваш CSV файл в формат как у файла `ml_rnd/data/credit_risk_dataset.csv`.
3. Изменить путь к CSV файлу в .env файле - в переменной `CSV_FILE_PATH`.
4. Используйте 
   - `task.ipynb` - ноутбук с предобработкой данных и выбором наилучшей модели для данных.
   - `my_processor.py` - файл с классом предобработки данных для пайплайна

### Для отладки
Отладка происходит через дебаггеры в контейнерах.
Рекомендуется использовать Visual Studio Code - присоединению к открытым портам для отслеживания испольнения отлаживаемого компонента проекта.
1. Перейдите в папку отладки:
   ```bash
   cd credit-risk-prediction/development
   ```
2. Соберите `Docker compose` проект:
   ```bash
   docker compose build
   docker compose up -d
   ```
3. Запустите приложениe streamlit для фронтэнда через браузер `localhost:8501`, дебаг через порт `5679`.
4. Дебаг приложения FastAPI для бекэнда через порт `5678`.

### Для получения предсказаний
1. Перейдите в папку продуктового окружения:
   ```bash
   cd credit-risk-prediction/production
   ```
2. Соберите `Docker compose` проект:
   ```bash
   docker compose build
   docker compose up -d
   ```
3. Запустите приложениe streamlit для фронтэнда через браузер `localhost:8501`.

# Credit Risk Prediction Project

## Overview

This is a machine learning project focused on credit risk prediction. The system analyzes financial data to predict the probability of default for personal loans, helping financial institutions make more informed lending decisions.

Used Kaggle datasets:
[Credit Risk Dataset](https://www.kaggle.com/datasets/laotse/credit-risk-dataset)

Notebook used as a basis for model selection:
[Credit Risk Prediction Training and EDA](https://www.kaggle.com/code/anshtanwar/credit-risk-prediction-training-and-eda)

## Key Features

- **Data Processing Pipeline**: Data cleaning and preprocessing combined with machine learning model in one object
- **Model Training**: Using scikit-learn library for model development and evaluation
- **Production Ready**: Backend ready for production deployment with Docker support
- **Interactive Frontend**: Streamlit-based interface for default prediction

The project uses an ML pipeline from scikit-learn with an ensemble of several shallow machine learning models, achieving the best metrics:
- Decision Tree
- Gradient Boosting Trees (CatBoost, LightGBM, Extreme Gradient Boosting)

Results of the trained ensemble on test data (20% of original sample):

| Metric                     | Value     |
|-----------------------------|-----------|
| Overall Accuracy            | 0.93      |
| Precision                   | 0.96      |
| Recall                      | 0.71      |
| Specificity                 | 0.99      |
| F1 Score                    | 0.82      |
| Additional Revenue          | 4,052,211.37 |

## Project Directory Structure

```
.
├── ml_rnd/                 # ML Research and Development
│   ├── src/                # R&D Code
│   ├── data/               # Dataset storage for model training
│   └── .env                # Environment variables for data processing and training
├── development/            # Development Environment
│   ├── backend/            # API Server
│   │   └── src/            # Development Code
│   │       └── model/      # Trained Models
│   └── frontend/           # Streamlit Application
│       └──  src/           # Development Code
└── production/             # Production Environment
    ├── backend/            # API Server
    │   └── src/            # Production Code
    │       ├── main.py     # FastAPI Application
    │       ├── db.py       # Database Operations
    │       └── model/      # Trained Models
    └── frontend/           # Streamlit Application
        └──  src/           # Production Code
```

## Technologies Used

- **Python 3.10+**: Main project language
- **Scikit-learn**: Primary machine learning library for training and evaluation
- **FastAPI**: Backend framework for providing predictions
- **Streamlit**: Interactive frontend for data exploration
- **Docker**: Containerization for project deployment
- **Pandas/NumPy**: Data manipulation and numerical computations

## Getting Started

### Requirements

- Git
- Docker (for container deployment)

### For Pipeline Development

#### Installation

Recommended to use Visual Studio Code.
1. Navigate to the repository folder:
   ```bash
   cd credit-risk-prediction
   ```

2. Set up virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: `.venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Navigate to the R&D code folder:
   ```bash
   cd ml_rnd/src
   ```

#### Model Training

1. Prepare your dataset in CSV format.
2. Format your CSV file to match `ml_rnd/data/credit_risk_dataset.csv`.
3. Change the path to your CSV file in the `.env` file - in the `CSV_FILE_PATH` variable.
4. Use:
   - `task.ipynb` - Notebook with data preprocessing and best model selection
   - `my_processor.py` - File with data preprocessing class for pipeline

### For Debugging

Debugging happens through debuggers in containers. Recommended to use Visual Studio Code - attach to open ports to track the execution of the component being debugged.
1. Navigate to the debugging folder:
   ```bash
   cd credit-risk-prediction/development
   ```

2. Build and start Docker compose project:
   ```bash
   docker compose build
   docker compose up -d
   ```

3. Launch Streamlit application for frontend via browser `localhost:8501`, debug through port `5679`.
4. Debug FastAPI application for backend through port `5678`.

### For Getting Predictions

1. Navigate to the production environment folder:
   ```bash
   cd credit-risk-prediction/production
   ```

2. Build and start Docker compose project:
   ```bash
   docker compose build
   docker compose up -d
   ```

3. Launch Streamlit application for frontend via browser `localhost:8501`.
