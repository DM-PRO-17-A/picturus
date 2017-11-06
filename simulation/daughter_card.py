from time import sleep


class Daughter_Card(object):
    def __init__(self):
        self.blocking_signs = ('r', 'l', 's')
        self.non_blocking_signs = ('5', '7', '1')
            
        self.actions = ("drive", "increase speed", "perform action", "looking for tape")
        self.effort = {"drive": 0.1, "increase speed": 1, "turn right": 3, "turn left": 3, "set speed to 50 km/h": 0.5, "set speed to 70 km/h": 0.5, "set speed to 100 km/h": 0.5, "stop": 0.2}
        self.state = self.actions[0]
        
        self.inputs = {'f': "drive", 'l': "look for tape", 'r': "turn right", 'l': "turn left", 's': "stop", '5': "set speed to 50 km/h", '7': "set speed to 70 km/h", '1': "set speed to 100 km/h"}


    def send(self, signal, prob):
        if prob < 0 or signal == 'f':
            self.state = self.inputs[signal]
            print "\tPCB: the QNN predicts that this is most likely not a relevant sign"
            return 0
            
        print "\tPCB: the QNN predicts the sign is a " + self.inputs[signal] + " with probability " + str(prob*100)
        
        if signal in self.blocking_signs:
            self.state = self.inputs[signal]
            return 3
        elif signal in self.non_blocking_signs:
            self.state = self.inputs[signal]
            return 2
        else:
            print "\tPCB: this is not an expected sign"
            self.state = self.inputs[signal]
            return 0

        
    def receive(self):
        print "\tPCB: performing action " + self.state
        sleep(self.effort[self.state])
        self.state = self.inputs['f']
