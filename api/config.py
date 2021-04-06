from http import HTTPStatus

from django.utils.translation import ugettext_lazy as _

NORTH = _("N")
EAST = _("E")
SOUTH = _("S")
WEST = _("W")

OPEN_WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

OPEN_WEATHER_RESPONSES = {
    HTTPStatus.OK: {"success": True},
    HTTPStatus.NOT_FOUND: {
        "success": False,
        "error_message": _("No entry found for this city"),
    },
    HTTPStatus.BAD_REQUEST: {
        "success": False,
        "error_message": _(
            "Bad request syntax or unsupported method - please raise an issue in the GitHub repo"
        ),
    },
    HTTPStatus.UNAUTHORIZED: {
        "success": False,
        "error_message": _(
            "Request unauthorised - please check you have set up your Open Weather API key correctly"
        ),
    },
    HTTPStatus.REQUEST_TIMEOUT: {
        "success": False,
        "error_message": _(
            "The Open Weather API is not available right now - please try again later"
        ),
    },
    HTTPStatus.INTERNAL_SERVER_ERROR: {
        "success": False,
        "error_message": _(
            "Internal Server Error - please raise an issue in the GitHub repo"
        ),
    },
    HTTPStatus.BAD_GATEWAY: {
        "success": False,
        "error_message": _(
            "Invalid response from another server/proxy - please raise an issue in the GitHub repo"
        ),
    },
}
