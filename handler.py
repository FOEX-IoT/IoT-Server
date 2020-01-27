from pytradfri import Gateway
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.error import PytradfriError
from pytradfri.util import load_json, save_json
from pytradfri.device import LightControl, Device, Light
from pytradfri.command import Command
import uuid


CONFIG_FILE = 'tradfri_standalone_psk.conf'


class Handler:
    def __init__(self, ip):
        conf = load_json(CONFIG_FILE)

        try:
            identity = conf[ip].get('identity')
            psk = conf[ip].get('key')
            api_factory = APIFactory(host=ip, psk_id=identity, psk=psk)
        except KeyError:
            raise EnvironmentError("Please generate a psk.conf file with"
                                   "the generate_tradfri_conf.py script")

        api = api_factory.request

        gateway = Gateway()

        try:
            dev_command = gateway.get_devices()
            dev_commands = api(dev_command)
            devices: [Device] = api(dev_commands)
            self.lights: [Light] = [
                dev for dev in devices if dev.has_light_control]
            light: Light = self.lights[0]
            print(light.name)
        except TypeError:
            print("re")
