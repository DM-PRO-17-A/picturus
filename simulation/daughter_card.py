from time import sleep

class Daughter_Card:
    gtsrb_classes = ['20 Km/h', '30 Km/h', '50 Km/h', '60 Km/h', '70 Km/h', '80 Km/h',
                     'End 80 Km/h', '100 Km/h', '120 Km/h', 'No overtaking',
                     'No overtaking for large trucks', 'Priority crossroad', 'Priority road',
                     'Give way', 'Stop', 'No vehicles',
                     'Prohibited for vehicles with a permitted gross weight over 3.5t including their trailers, and for tractors except passenger cars and buses',
                     'No entry for vehicular traffic', 'Danger Ahead', 'Bend to left',
                     'Bend to right', 'Double bend (first to left)', 'Uneven road',
                     'Road slippery when wet or dirty', 'Road narrows (right)', 'Road works',
                     'Traffic signals', 'Pedestrians in road ahead', 'Children crossing ahead',
                     'Bicycles prohibited', 'Risk of snow or ice', 'Wild animals',
                     'End of all speed and overtaking restrictions', 'Turn right ahead',
                     'Turn left ahead', 'Ahead only', 'Ahead or right only',
                     'Ahead or left only', 'Pass by on right', 'Pass by on left', 'Roundabout',
                     'End of no-overtaking zone',
                     'End of no-overtaking zone for vehicles with a permitted gross weight over 3.5t including their trailers, and for tractors except passenger cars and buses']
    
    blocking_signs = ("Turn left ahead", "Turn right ahead", "Stop")
    non_blocking_signs = ("50 Km/h")
    
    
    actions = ("drive", "increase speed", "perform action")
    effort = {"drive": 0.5, "increase speed": 1, "perform action": 3}
    state = actions[0]
        

    def send(self, result):
        #f = open('probs.txt', 'a')
        temp_max = -1
        index = -1
        for i in range(len(result)):
            #if int(result[i]*100) != 0:
            #    f.write(self.gtsrb_classes[i] + " with probability "+str(int(result[i]*100))+'%' '\n')
            if result[i] > temp_max:
                temp_max = result[i]
                index = i
                sign = self.gtsrb_classes[index]
        print "\tPCB: the QNN predicts the sign is a " + sign + " with probability " + str(temp_max*100)
        #f.write('\n')
        #f.close()
        if sign in self.blocking_signs:
            state = self.actions[2]
            return 3
        elif sign in self.non_blocking_signs:
            state = self.actions[1]
            return 2
        else:
            print "\tPCB: this is not an expected sign"
            state = self.actions[0]
            return 0
                
    def receive(self):
        print "\tPCB: performing action " + self.state
        sleep(self.effort[self.state])
        state = self.actions[0]
