from datetime import datetime


class DateTimeHelpers:

    def get_server_datetime(self):
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return str(dt)