#include <string>
#include <algorithm>
#include <map>
// Rosetta stuff in order to use the pins
//#include "TestRegOps.hpp"
#include "platform.h"


const std::string gtsrb_classes[43] = {'20 Km/h', '30 Km/h', '50 Km/h', '60 Km/h', '70 Km/h', '80 Km/h',
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
				 'End of no-overtaking zone for vehicles with a permitted gross weight over 3.5t including their trailers, and for tractors except passenger cars and buses'};


struct Sign
{
	int[2] action = {0, 0};
};
int[2] speed = {0, 0};

std::map <std::string, Sign> signals;
signals["50 Km/h"] = new Sign;
signals["70 Km/h"] = new Sign;
signals["100 Km/h"] = new Sign;


int* get_signal( std::string sign )
{
	int[4] signal;
	if ( "50 Km/h" == sign )
}


int main()
{
	// Platform to use pins from
	WrapperRegDriver * platform = initPlatform();
	AutoSimple t( platform );


	while ( 1 == get_pcb_btn() );

	
	float[43] average;
	int i;
	for ( i = 0; i < 43; ++i )
		average[i] = 0.0;
	const int N = sizeof(average) / sizeof(float);
	

	while(1)
	{
		int[2] input = get_input_pins( t );
		if ( 1 == input[1] )
			continue;

		
		// Read from QNN output
		float[43] output = get_qnn_output( platform );
		int i;
		for ( i = 0; i < 43; ++i )
		{
			// Insert logic for calculating most likely sign
			average[i] += output[i];
		}
		int max_index = max_element( average, average + N );

		std::string sign = gtsrb_classes[max_index];
	}
	

	deinitPlatform(platform);
	
	
	return 0;
}
