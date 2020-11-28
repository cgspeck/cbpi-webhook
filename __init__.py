from modules import cbpi  # , app
import requests

webhook_endpoint = None
webhook_ok = False


def webhookEndpoint():
    global webhook_endpoint
    webhook_endpoint = cbpi.get_config_parameter("webhook_endpoint", None)
    if webhook_endpoint is None:
        try:
            cbpi.add_config_parameter(
                "webhook_endpoint",
                "http://192.168.1.6:1880/cbpi",
                "text",
                "Endpoint to post events to",
            )
        except:
            cbpi.notify(
                "Webhook Error",
                "Unable to update database. Update CraftBeerPi and reboot.",
                type="danger",
                timeout=None,
            )


@cbpi.initalizer(order=9000)
def init(cbpi):
    global webhook_ok
    cbpi.app.logger.info("INITIALIZE Webhook PLUGIN")
    webhookEndpoint()
    if webhook_endpoint is None or not webhook_endpoint:
        cbpi.notify(
            "Webhook Error",
            "Webhook Endpoint is not set",
            type="danger",
            timeout=None,
        )
    else:
        webhook_ok = True


@cbpi.event("MESSAGE", async=True)
def messageEvent(message):
    global webhook_ok
    global webhook_endpoint
    memo = {}
    memo["message"] = message["message"]
    memo["title"] = message["headline"]
    requests.post(webhook_endpoint, json=memo)
