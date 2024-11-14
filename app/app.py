from views import (
    AdView,
    AdViewError,
    handle_invalid_adview_usage,
    handle_invalid_usage,
    hello_world,
)

from flask import Flask

app = Flask("my_app")

app.add_url_rule(
    "/",
    view_func=hello_world,
    methods=["GET"]
)
app.add_url_rule(
    "/advertisements/",
    view_func=AdView.as_view("advertisements_create"),
    methods=["POST"],
)
app.add_url_rule(
    "/advertisements/<int:id_ad>/",
    view_func=AdView.as_view("advertisements_delete"),
    methods=["DELETE"],
)
app.add_url_rule(
    "/advertisements/<int:id_ad>/",
    view_func=AdView.as_view("advertisements_get"),
    methods=["GET"],
)

handle_invalid_adview_usage = \
    app.errorhandler(AdViewError)(handle_invalid_adview_usage)
handle_invalid_usage = \
    app.errorhandler(Exception)(handle_invalid_usage)


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
