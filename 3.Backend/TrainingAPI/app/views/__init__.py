from sanic import Blueprint, Sanic


def route(sanic_app: Sanic):
    from app.views.sample import sample

    api_v1_blueprint = Blueprint('api_v1', url_prefix='/api/v1')

    api_v1_blueprint.add_route(sample.Sample.as_view(), '/sample')

    sanic_app.blueprint(api_v1_blueprint)
