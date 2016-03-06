import requests
import urllib


class BuycraftAPI(object):
    def __init__(self, secret, url='https://plugin.buycraft.net'):
        """
        Creates a new BuycraftAPI instance.

        :param secret: the server's secret, available from https://server.buycraft.net/servers
        :param url: URL for the Buycraft API, default is https://plugin.buycraft.net
        """
        self.api_key = secret
        self.url = url

    def _getjson(self, url):
        return requests.get(url, headers={'X-Buycraft-Secret': self.secret}).json()

    def information(self):
        """Returns information about the server and the webstore.
        """
        return self._getjson(self.url + '/information')

    def listing(self):
        """Returns a listing of all packages available on the webstore.
        """
        return self._getjson(self.url + '/listing')

    def get_due_players(self, page=None):
        """Returns a listing of all players that have commands available to run.

        :param page: the page number to use
        """
        if page is None:
            return self._getjson(self.url + '/queue')
        elif isinstance(page, int):
            return self._getjson(self.url + '/queue?page=' + str(page))
        else:
            raise Exception("page parameter is not valid")

    def get_offline_commands(self):
        """Returns a listing of all commands that can be run immediately.
        """
        return self._getjson(self.url + '/queue/offline-commands')

    def get_player_commands(self, player_id):
        """Returns a listing of all commands that require a player to be run.
        """
        if isinstance(player_id, int):
            return self._getjson(self.url + '/queue/online-commands/' + str(player_id))
        else:
            raise Exception("player_id parameter is not valid")

    def mark_commands_completed(self, command_ids):
        """Marks the specified commands as complete.

        :param command_ids: the IDs of the commands to mark completed
        """
        ids = urllib.urlencode(map(lambda id: ("ids[]", id), command_ids))
        return requests.delete(self.url + '/queue?' + ids)

    def recent_payments(self, limit):
        """Gets the rest of recent payments made for this webstore.

        :param limit: the maximum number of payments to return. The API will only return a maximum of 100.
        """
        if isinstance(limit, int):
            return self._getjson(self.url + '/payments')
        else:
            raise Exception("limit parameter is not valid")
