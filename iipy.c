/* Copyright (C) 2012-2013 Teodor Spæren <teodor_spaeren@lavabit.com>
 * Licensed under the 2-clause BSD license, see LICENSE. */
#include <Python.h>
#include <signal.h>

#define IIPY_EVENTLOADER "eventLoad"
#define IIPY_INIT "main"
#define IIPY_MANAGER "iipy"

int
Load_PythonFunc(char* sModule, char* sFunc, PyObject *pArgs)
{
    PyObject *pName, *pModule, *pFunc, *pValue;

    // Starting up the module
    pName = PyUnicode_FromString(sModule);

    pModule = PyImport_Import(pName);
    Py_DECREF(pName);
    
    if(pModule != NULL) {
        pFunc = PyObject_GetAttrString(pModule, sFunc);
        
        if(pFunc && PyCallable_Check(pFunc)) {
            // Here the actuall call is made
            pValue = PyObject_CallObject(pFunc, pArgs);
            if(pValue != NULL) {
                //printf("Python plugins loaded with return value: %ld\n", PyLong_AsLong(pValue));
                Py_DECREF(pValue);
            }
            else {
                Py_DECREF(pFunc);
                Py_DECREF(pModule);
                PyErr_Print();
                fprintf(stderr, "Call failed\n");
                return -1;
            } // END OF pValue call
        } // END OF pFunc && PyCallable_Chjeck()
        else {
            if (PyErr_Occurred()) {
                PyErr_Print();
            }
            fprintf(stderr, "Cannot find function \"%s\"\n", sFunc);
        } // END OF function checking

        // We don't need these any more.
        Py_XDECREF(pFunc);
        Py_DECREF(pModule);
    } // END OF successful module find
    else {
        PyErr_Print();
        fprintf(stderr, "Failed to load \"%s\"\n", sModule);
        return -1;
    }
    return 0;
}

/* Abstraction layer for sending events *
 * This expects the info variable to be a tuple */
int
iipy_LoadEvent(PyObject *info)
{
    // We need to pack the tuple once more so that it get passed as a tuple
    // to the event manager
    int res = Load_PythonFunc(IIPY_MANAGER, IIPY_EVENTLOADER, info);
    Py_DECREF(info);
    return res;
}

/* Fires of the Spoke event and returns -1 on error */
int
iipy_SpokeEvent(char* channel, char* msg)
{
    PyObject *eventdata;
    
    // We need to build the tuple that we are sending off to the event loader
    eventdata = Py_BuildValue("s s s", "spoke", channel, msg);
    if(eventdata) {
        int res = iipy_LoadEvent(eventdata);
        Py_DECREF(eventdata);
        return res;
    }

    return -1;
}
/* This is the function that is responsible for starting up the python
 * interpreter.
 */
int
Load_Python(void)
{
    Py_Initialize();
    
    /* Adding the plugin folder to the import path */
    PyRun_SimpleString("import sys\n" "sys.path.append('plugins/')\n");

    /* Calling the manager. */
    int res = Load_PythonFunc(IIPY_MANAGER, IIPY_INIT, NULL);
    
    return res;
}

