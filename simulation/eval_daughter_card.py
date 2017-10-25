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

    gtsrb_subset = ['50 Km/h','70 Km/h','80 Km/h','100 Km/h','Stop','Turn left ahead','Turn right ahead']
    
    actions = ("drive", "increase speed", "perform action")
    effort = {"drive": 0.5, "increase speed": 1, "perform action": 3}
    state = actions[0]

    subset_probs = {'50 Km/h':[],'70 Km/h':[],'80 Km/h':[],'100 Km/h':[],'Stop':[],'Turn left ahead':[],'Turn right ahead':[]}
        
    def send(self, result):
        for i in range(len(result)):
            if int(result[i]*100) != 0:
                sign = self.gtsrb_classes[i]
                if sign in self.gtsrb_subset:
                    if int(result[i]*100)>15:
                        self.subset_probs[sign].append(result[i])
                    else:
                        self.subset_probs[sign].append(0)
        return 0
                
    def receive(self):
        state = self.actions[0]
