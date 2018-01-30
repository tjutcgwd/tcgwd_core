# -*- coding: utf-8 -*-

import json
import requests


class Address(object):

    def __init__(self, address=None, location=None):
        self._address = address
        self._location = location
        self._component = None
        self._base_url = "http://api.map.baidu.com"
        self._params = {'output': 'json', 'ak': 'GRlG8i8IeHcupO8GR77s5LHGPk27kBlT'}

    @property
    def address(self):
        return self._get_address()

    @property
    def location(self):
        return self._location if self._location else self._get_location()

    @property
    def province(self):
        self._set_address()
        return self._component['province']

    @property
    def city(self):
        self._set_address()
        return self._component['city']

    @property
    def district(self):
        self._set_address()
        return self._component['district']

    def route(self, address):
        return self._get_route_info(address)

    def _set_address(self):
        if not self._component:
            self._address = self._get_address()

    def _get_route_info(self, address):
        func_url = '/routematrix/v2/driving'
        origin = ','.join(map(str, self.location))
        destination = ','.join(map(str, address.location))
        params = self._params.copy()
        params.update(origins=origin, destinations=destination)

        result = requests.get(self._base_url + func_url, params=params)
        data = json.loads(result.text)
        if data['status'] == 0:
            return {
                'duration': data['result'][0]['duration']['value'],
                'distance': data['result'][0]['distance']['value']
            }
        else:
            return None

    def _get_location(self):
        func_url = '/geocoder/v2/'
        params = self._params.copy()
        params.update(address=self._address)

        result = requests.get(self._base_url + func_url, params)
        data = json.loads(result.text)
        if data['status'] == 0:
            return data['result']['location']['lat'], data['result']['location']['lng'],
        else:
            return None

    def _get_address(self):
        if not self._component:
            func_url = '/geocoder/v2/'
            params = self._params.copy()
            params.update(location=",".join(map(str, self.location)))

            result = requests.get(self._base_url + func_url, params)
            data = json.loads(result.text)
            if data['status'] == 0:
                self._component = data['result']['addressComponent']
                self._address = data['result']['formatted_address'] + data['result']['sematic_description']
            else:
                return None
        return self._address


if __name__ == "__main__":
    # example

    addr = Address(address="金隅嘉华大厦")
    print(addr.address)
    print(addr.location)
    print(addr.province)
    print(addr.city)
    print(addr.district)
    print()

    addr_2 = Address(location=(40.07871264866282, 116.33392797379916))
    print(addr_2.address)
    print(addr_2.location)
    print(addr_2.province)
    print(addr_2.city)
    print(addr_2.district)
    print()

    print(addr_2.route(addr))
    print(Address.route(addr_2, addr))