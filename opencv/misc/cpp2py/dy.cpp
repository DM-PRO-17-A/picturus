#include <Python.h>

int
main(int argc, char *argv[])
{
  // Py_SetProgramName(argv[0]);  /* optional but recommended */
  Py_Initialize();
  FILE* file = fopen("how.py","r");
  PyRun_SimpleFile(file, "how.py");
  Py_Finalize();
  return 0;
}
