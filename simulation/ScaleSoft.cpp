#include <iostream>
#include <cmath>
#include <iomanip>
#include <fstream>
#include <string>
#include <sstream>
#include <cstdlib>
#include <Python.h>
using namespace std;
static PyObject *





float* run(PyObject *self, PyObject *args){
	//Hente data fra fil/BRAM
	
	ifstream file;
	file.open("./Scalshiftinput.txt"); // laster 43 int fra en fil evt BRAM
	string line;
	float input[43];

	if (file.is_open()) // Leser og setter inn tallene i en array
  	{
    	for (int i =0; i < 43; i = i+1){	
    		getline(file,line); 
      		float temp = std::stof(line);
      		input[i] = temp;
  
    	};
    	file.close();
  	}

  	else cout << "Unable to open file 1";

	file.close();

	//#############################################################################################
	//SCALESIFT

	//filter 1
    float A[43] = {0.10613798, 0.0967258, 0.0944901, 0.08205982, 0.08600254, 0.07336438,
  					0.09290288, 0.08346851, 0.08365503, 0.10139856, 0.09375499, 0.10817018,
					0.12580705, 0.11591881, 0.10589285, 0.1045065,  0.09333096, 0.10654855,
					0.09912547, 0.09181008, 0.10024401, 0.10732551, 0.09640726, 0.102323,
					0.11001986, 0.10809018, 0.09999774, 0.10208429, 0.0995523,  0.11225812,
					0.10275448, 0.09403487, 0.10364552, 0.10415483, 0.10874164, 0.12092833,
					0.10799013, 0.09335944, 0.1140102,  0.09289351, 0.11192361, 0.09586933,
					0.08955998};
	//filter 2
	float B[43] = {-0.96071649, 0.68546766, 1.44876862, 1.84089804, 1.4770503, 2.17828822,
					 -0.48416716, 0.3688474, 1.08563411, 0.55420429, 0.43626797, 0.16900358,
					 -0.1347385,  0.0145933, -0.54196042, -0.37247148, -0.58978826, -0.4172011,
					  0.26940933, -0.02862083, 0.28240931, -0.60368943, -0.63643998,  0.05946794,
					 -0.21361144, 0.09381656, -0.09491161, -0.64013398,  0.05029509, -0.51663965,
					 -0.32239845, 0.43873206, -0.75330114, -0.14596492, -0.45224375, -0.29807806,
					 -0.57703501, -0.58822173, 0.20007333, -0.55777472, -0.56918406, -0.59853441,
					 -0.55538076};
    float inn[43]; // tall etter at scaleshift har kjort
    
    for (int i =0; i < 43; i = i+1){ 
    	inn[i]= input[i]*A[i] + B[i];
    };
    // #############################################################################################
    //SOFTMAX

    float out [43]; // De endelige 43 tallene etter softmax
	

	float sum = 0;
	float max = inn[0];
	for (int i =0; i < 43; i = i+1){
		if(inn[i] > max){
			max = inn[i];
		};
	};
	std::cout << std::fixed;
	std::cout << std::setprecision(14);

	for (int i =0; i < 43; i = i+1){ 	
   		out[i] = std::exp(inn[i] - max); 
   		sum = sum + out[i];

    };
    for (int i =0; i < 43; i = i+1){
   		//cout << max << " -- " << sum << " -- " << out[i];
   		out[i] = out[i] / sum;
   		
    };
    // #############################################################################################
    //Write to file
    float* pointer = out;

    return PyLong_FromLong(pointer);
}


int main() {
	run();
	return 0;
}