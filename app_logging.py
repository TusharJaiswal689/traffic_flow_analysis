import logging

# # Configure logging to save to a file
# logging.basicConfig(
#     filename="app.log",
#     encoding="utf-8",
#     level=logging.DEBUG,
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )

# 1. Create a custom logger variable
logger = logging.getLogger("traffic_flow")
logger.setLevel(logging.DEBUG)

# 2. Create a file handler to save logs to a file
file_handler = logging.FileHandler("app.log", "a", "utf-8")
file_handler.setLevel(logging.DEBUG)

# 3. Create a formatter and attach it to the handler
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)

# 4. Add the handler to logger variable
logger.addHandler(file_handler)

