import odoo.tests
from odoo.tests import HttpCase, tagged, mute_logger


@tagged('post_install', '-at_install')
class TestSafetyControlController(odoo.tests.HttpCase):

    @mute_logger('odoo.http')
    def test_controllers(self):
        request = self.url_open('/safety/create_alert')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json(), {
                        "jsonrpc": "2.0",
                        "method": "call",
                        "params": {
                            "time": "Wed Dec 14 2022 12:01:10 GMT+0300",
                            "lastTime": "Wed Dec 14 2022 12:01:10 GMT+0300",
                            "image": "data:image/jpeg;base64,testphoto",
                                "recognitionType": [
                                    "no_helmet",
                                    "no_gloves"
                                ],
                                "device": "Iphone 13",
                                "personWithoutHelmet": True,
                                "personWithoutHeadphones": True,
                                "personWithoutJacket": False,
                                "personWithoutGloves": True,
                                "personWithoutMask": False
                            }})
