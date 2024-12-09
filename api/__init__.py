from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI()

    from api.sounds import sounds_router
    app.include_router(sounds_router, prefix="/sounds")

    # from api.users import users_router
    # app.include_router(users_router)
                       
    return app