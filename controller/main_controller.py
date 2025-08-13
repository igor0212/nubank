class MainController:
    def __init__(self, service):
        self.service = service

    def handle_request(self, data):
        # ...existing code...
        return self.service.process(data)