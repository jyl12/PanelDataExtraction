from opcua import Server
import time
from random import randint

class ExtendedServer(Server):
    def __init__(self,port):
        super().__init__()
        ip = "192.168.0.135"
        self.url = "opc.tcp://" + str(ip) + ":" + str(port)
        self.set_endpoint(self.url)
        name = "opcua_simulation_server"
        self.addspace = self.register_namespace(name)
        print("namespace is:", self.addspace)
        
    def testfunc(self , objectname = "Parters" , variablename = "Varie" ): #incomplete
        print("test")
        node = server.get_objects_node()
        print("node is:", node)
        print("test2")

def opcuaserver_settings(objectname = "Parameters" , variablename = "Variable"):
    global Temp
    node = server.get_objects_node()
    print("node is:", node)
    param = node.add_object(server.addspace, objectname)
    print("param is:",param)
    Temp = param.add_variable (server.addspace, variablename, 0)
    server.start()
    print("Server is started at {}".format(server.url))

if __name__ == "__main__":
    server = ExtendedServer(4840)
    opcuaserver_settings("test_para","test_var")
    # node = server.get_objects_node()
    # print("node is:", node)
    # param = node.add_object(server.addspace, "Parameters")
    # print("param is:",param)
    # Temp = param.add_variable (server.addspace, "Temperature", 0)
    # server.start()
    # print("Server is started at {}".format(server.url))
    while True:  
        Temperature = randint(10, 50)
        print("Temperature:",Temperature)
        Temp.set_value(Temperature)
        time.sleep(2)