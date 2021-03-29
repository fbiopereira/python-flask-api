from datetime import datetime


class DateTimeHelpers:

    @staticmethod
    def get_server_datetime():
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return str(dt)