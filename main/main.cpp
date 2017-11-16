#include <string>
// Rosetta stuff in order to use the pins
#include "TestRegOps.hpp"
#include "platform.h"


const string gtsrb_classes[43] = {'20 Km/h', '30 Km/h', '50 Km/h', '60 Km/h', '70 Km/h', '80 Km/h',
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
                 'End of no-overtaking zone for vehicles with a permitted gross weight over 3.5t including their trailers, and for tractors except passenger cars and buses'}


int main()
{
	// Platform to use pins from
	WrapperRegDriver * platform = initPlatform();
	TestRegOps t(platform);
	/* In order to write to pins, use:
	   t.set_out_pins(n);
	   Where n is a number that gets translated to binary
	   E.g.: 12 => 1100
	 */
	

	
	float[43] average;
	int i;
	for ( i = 0; i < 43; ++i )
		average[i] = 0.0;


	// Initialise camera program here? Or separately in Bash?

	
	while(1)
	{
		// Read from QNN output
		// float[43] output = QNN_output;
		int i;
		for ( i = 0; i < 43; ++i )
			average[i] += output[i];
	}
	

	deinitPlatform(platform);
	
	
	return 0;
}
