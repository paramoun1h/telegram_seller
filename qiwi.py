from abc import ABC, abstractmethod
import requests
import json


class QiwiBase(ABC):

    def user_profile(self, headers):
        response = requests.get(
            'https://edge.qiwi.com/person-profile/v1/profile/current?parameter=value',
            headers=headers)
        try:
            return response.json()
        except json.JSONDecodeError:
            return None

    def load_history(self, headers, wallet):
        response = requests.get(
            f'https://edge.qiwi.com/payment-history/v2/persons/{wallet}'
            f'/payments?rows=50&operation=IN&sources=QW_RUB',
            headers=headers)
        return response.json()

    @abstractmethod
    def find_pay(self, comment, my_list):
        pass


class Qiwi(QiwiBase):
    def __init__(self, token):
        self.token = token
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json',
                        'Authorization': f'Bearer {token}'}
        self.user_number = ''

    def get_profile(self):
        element = self.user_profile(self.headers)
        if element:
            self.user_number = element['authInfo']['personId']
            return element['authInfo']['personId']
        else:
            self.user_number = None
            return False

    def get_history(self):
        result = self._check_element()
        if result:
            return result(self.headers, self.user_number)
        else:
            return False

    def _check_element(self):
        if type(self.user_number) == int and self.user_number is not None:
            return self.load_history
        elif self.user_number is not None:
            if self.get_profile():
                return self.load_history
        else:
            return False

    def find_pay(self, comments_input, my_list):
        for i in my_list['data']:
            if i['comment'] == comments_input:
                return i

