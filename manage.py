from application.init_app import app, init_app, manager
from application import views  # noqa


if __name__ == "__main__":
    init_app(app)
    manager.run()
