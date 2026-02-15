# Проект по прогнозированию кредитного риска

## Обзор

Это проект в области машинного обучения, направленный на прогнозирование кредитных рисков. Система анализирует финансовые данные для предсказания вероятности дефолта взятого частным лицом кредита, что помагает финансовым учреждениям принимать более обоснованные решения при выдаче кредитов.

Использованные данные Kaggle: https://www.kaggle.com/datasets/laotse/credit-risk-dataset
Ноутбук, который был взят за основу для выбора модели: https://www.kaggle.com/code/anshtanwar/credit-risk-prediction-training-and-eda

## Ключевые особенности

- **Пайплайн обработки данных**: Очистка и предобработка кредитных данных для обучения модели и предсказания 
- **Обучение моделей**: Использование библиотеки scikit-learn для разработки и оценки моделей
- **Готовность к развертыванию**: Бэкенд, готовый к производственному развертыванию с поддержкой Docker
- **Интерактивный фронтенд**: Интерфейс на основе Streamlit для предсказания дефолта по данным

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
└── production/             # Развертывание в производственной среде
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
- **Docker**: Контейнеризация для развертывания
- **Pandas/NumPy**: Манипуляция данными и численные вычисления

## Начало работы

### Требования

- Git
- Docker (для контейнерного развертывания)

### Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ilyadash/simple-credit-score.git
   cd credit-risk-prediction
   ```

2. Настройте виртуальную среду и установите зависимости:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # На Windows используйте `.venv\Scripts\activate`
   pip install -r requirements.txt
   ```

## Использование

### Для обучения модели

1. Подготовьте ваш набор данных в формате CSV (см. `ml_rnd/data/credit_risk_dataset.csv` как пример)
2. Запустите скрипт обучения:
   ```bash
   python -m ml_rnd.src.task train --data_path path/to/your/data.csv
   ```

### Для получения предсказаний

Бэкенд на FastAPI предоставляет эндпоинты для предсказаний. После запуска сервера:

```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={"features": [0.1, 0.2, ...]}  # Ваши значения признаков
)
print(response.json())
```

### Исследование данных

Запустите приложение Streamlit для визуализации данных:
```bash
cd development/frontend
streamlit run src/streamlit_app.py
```

## Компоненты проекта

### Обработка данных

Модуль `my_processor.py` содержит пользовательскую логику предобработки кредитных данных, включая:
- Инженерию признаков
- Обработку пропущенных значений
- Нормализацию/масштабирование
- Кодирование категориальных переменных

### Обучение моделей

Проект использует машинный пайплайн scikit-learn с распространенными алгоритмами:
- Случайный лес (Random Forest)
- Градиентное бустинговое дерево (CatBoost)
- Логистическая регрессия
- Метод опорных векторов (SVM)

### Метрики оценки

Ключевые метрики производительности:
- Точность/Полнота/F1-мера
- ROC-AUC показатель
- Матрица ошибок
- Бизнес-специфические метрики (например, PD, LGD)

## Вклад в проект

Вклады приветствуются! Пожалуйста, следуйте этим шагам:

1. Форкните проект
2. Создайте вашу фичу (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Запушьте в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## Лицензия

Этот проект лицензируется под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## Контакты

Для вопросов или поддержки обращайтесь:
- Лид проекта: [Ваше имя]
- Электронная почта: [Ваш email]

---

# Credit Risk Prediction Project

## Overview

This is a machine learning project focused on credit risk prediction. The system analyzes financial data to predict the likelihood of loan defaults, helping financial institutions make more informed lending decisions.

## Key Features

- **Data Processing Pipeline**: Clean and preprocess credit data using custom processors
- **Model Training**: Uses scikit-learn for model development and evaluation
- **Deployment Ready**: Production-ready backend with Docker support
- **Interactive Frontend**: Streamlit-based interface for data exploration

## Project Structure

```
.
├── ml_rnd/                # Machine learning research & development
│   ├── src/               # Source code
│   │   ├── my_processor.py  # Custom data processing logic
│   │   └── __init__.py
│   ├── data/              # Dataset storage
│   │   └── credit_risk_dataset.csv
│   └── task.ipynb         # Jupyter notebook for analysis
├── development/           # Development environment
│   ├── backend/           # API server
│   │   ├── src/
│   │   │   ├── main.py    # FastAPI application
│   │   │   ├── db.py      # Database operations
│   │   │   └── model/     # Trained models
│   └── frontend/          # Streamlit app
├── production/            # Production deployment
└── requirements.txt       # Python dependencies
```

## Technologies Used

- **Python 3.8+**
- **Scikit-learn**: Core machine learning library for model training and evaluation
- **FastAPI**: Backend web framework for serving predictions
- **Streamlit**: Interactive frontend for data exploration
- **Docker**: Containerization for deployment
- **Pandas/NumPy**: Data manipulation and numerical computing

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Docker (for containerized deployment)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd credit-risk-prediction
   ```

2. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. For development setup (optional):
   ```bash
   cd development/backend
   docker-compose up --build
   ```

## Usage

### Training the Model

1. Prepare your dataset in CSV format (see `ml_rnd/data/credit_risk_dataset.csv` as reference)
2. Run the training script:
   ```bash
   python -m ml_rnd.src.task train --data_path path/to/your/data.csv
   ```

### Making Predictions

The FastAPI backend provides prediction endpoints. After starting the server:

```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={"features": [0.1, 0.2, ...]}  # Your feature values
)
print(response.json())
```

### Exploring Data

Run the Streamlit app to visualize your data:
```bash
cd development/frontend
streamlit run src/streamlit_app.py
```

## Project Components

### Data Processing

The `my_processor.py` module contains custom preprocessing logic for credit data, including:
- Feature engineering
- Handling missing values
- Normalization/scaling
- Categorical variable encoding

### Model Training

The project uses scikit-learn's machine learning pipeline with common algorithms like:
- Random Forest
- Gradient Boosting (CatBoost)
- Logistic Regression
- Support Vector Machines

### Evaluation Metrics

Key performance metrics tracked:
- Precision/Recall/F1-score
- ROC-AUC score
- Confusion matrix analysis
- Business-specific metrics (e.g., PD, LGD)

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact:
- Project Lead: [Your Name]
- Email: [Your Email]

---

**Note**: This README provides an overview. For detailed implementation specifics, refer to the code comments and documentation within each module.