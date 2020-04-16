#### CLIENT CLASS
class Client():
    def __init__(self):
        self.reset()

    def reset(self):
        self.client_id = 0
        self.client_key = None
        self.client_secret = None
        self.status = None

    def serialize(self):
        return {
            "client_id": self.client_id,
            "client_key": self.client_key,
            "client_secret": self.client_secret,
            "status": self.status
        }


class Clients():

    clients = []

    def __init__(self):
        for index in range(15):
            client = Client()
            client.client_id = index+1
            client.client_key = f"CLIENT0{index+1}"
            client.client_secret = f"SECRET0{index+1}"
            client.status = True
            self.clients.append(client.serialize())

    def get_clients(self):
        return self.clients

    def add(self, string):
        self.clients.append(string)

    def get_one(self, client_id):
        for _, value in enumerate(self.persons):
            if int(value["client_id"]) == int(client_id):
                return value
        return None

    def edit_one(self, client_id, client_key, client_secret, status):
        for index, value in enumerate(self.clients):
            if int(value["client_id"]) == int(client_id):
                client = Client()
                client.client_id = client_id
                client.client_key = client_key if client_key != None else value["client_key"]
                client.client_secret = client_secret if client_secret != None else value[
                    "client_secret"]
                client.status = status if status != None else value["status"]
                self.clients[k] = client.serialize()
                return client
        return None

    def delete_one(self, client_id):
        for index, value in enumerate(self.clients):
            if int(value["client_id"]) == int(client_id):
                self.clients.pop(index)
                return True
        return None
