from time import sleep


class Daughter_Card:
    
    # blocking_signs = ("Turn right ahead", "Turn left ahead", "Stop")
    # non_blocking_signs = ("50 Km/h")
    blocking_signs = ('r', 'l', 's')
    non_blocking_signs = ('5')
    
    
    actions = ("drive", "increase speed", "perform action", "looking for tape")
    effort = {"drive": 0.5, "increase speed": 1, "perform action": 3}
    state = actions[0]
        

    inputs = {'d': "drive", 'l': "look for tape", 'r': "turn right", 'l': "turn left", 's': "stop", '5': "setting speed to 50 km/h"}

    def send(self, signal, prob):
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
        # TODO: fix effort
        print "\tPCB: performing action " + self.state
        sleep(self.effort[self.state])
        self.state = self.inputs['d']
