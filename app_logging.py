import logging

# 1. Create a custom logger variable
logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)

# 2. Create a file handler to save logs to a file
file_handler = logging.FileHandler("logs/app.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# 3. Create a formatter and attach it to the handler
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)

# 4. Add the handler to logger variable
logger.addHandler(file_handler)

