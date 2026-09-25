from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str

    APP_ENV: str

    DATABASE_HOST: str

    DATABASE_PORT: int

    DATABASE_NAME: str

    DATABASE_USER: str

    DATABASE_PASSWORD: str


    class Config:
        env_file=".env"


settings = Settings()


print("========================")
print("DATABASE HOST:", settings.DATABASE_HOST)
print("DATABASE PORT:", settings.DATABASE_PORT)
print("DATABASE NAME:", settings.DATABASE_NAME)
print("DATABASE USER:", settings.DATABASE_USER)
print("DATABASE PASSWORD:", repr(settings.DATABASE_PASSWORD))
print("========================")