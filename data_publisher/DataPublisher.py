import threading
import paho.mqtt.client as mqtt

lock = threading.Lock()

class DataPublisher:
    def __init__(self):
        self.client = mqtt.Client("jcermak")
        self.client.connect("172.22.32.140")

    def send_data(self, data):
        data = self.__process_data(data)
        try:
            lock.acquire()
            self.client.publish("test", data) 
            lock.release()
        except Exception as e:
            return None

    def __process_data(self, data):
        if not isinstance(data, str):
            data = str(data)
        if not data.endswith("\n"):
            data += "\n"
        return data

    def send_data_array(self, data_array):
        data_string = self.__process_data_array(data_array)
        self.send_data(data_string)

    def __process_data_array(self, data_array):
        data_string = ""
        for data in data_array:
            data_string += str(data)
            data_string += ","
        return data_string

    def read_data(self):
        try:
            lock.acquire()
            with self.serial as serial:
                data = serial.readline().decode()
            lock.release()
        except Exception as e:
            return None
        if data == "":
            return None
        if data != "":
            self.serial_data_array = data.split(",")
        else:
            self.serial_data_array[0] = data
        return self.serial_data_array
