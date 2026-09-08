from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://iot_user:iot_password@localhost:5432/iot_monitoring"
    mqtt_broker_host: str = "localhost"
    mqtt_broker_port: int = 1883

settings = Settings()