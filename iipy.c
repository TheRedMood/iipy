/* Copyright (C) 2012-2013 Teodor Spæren <teodor_spaeren@lavabit.com>
 * Licensed under the 2-clause BSD license, see LICENSE. */
#include <Python.h>
#include <signal.h>

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
        /* P func is a new referance */
        
        if(pFunc && PyCallable_Check(pFunc)) {
            // Here the actuall call is made
            pValue = PyObject_CallObject(pFunc, pArgs);
            if(pValue != NULL) {
                printf("Python plugins loaded with return value: %ld\n", PyLong_AsLong(pValue));
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

        // We don't need these anymore.
        Py_XDECREF(pFunc);
        Py_DECREF(pModule);
    } // END OF succsessfull module find
    else {
        PyErr_Print();
        fprintf(stderr, "Failed to load \"%s\"\n", sModule);
        return -1;
    }
    return 0;
}

//int

/* This is the function that is responsible for starting up the python
 * interpeter.
 */
int
Load_Python(void)
{
    Py_Initialize();
    
    /* Adding the plugins folder to the import path */
    PyRun_SimpleString("import sys\n" "sys.path.append('plugins/')\n");
    int res = Load_PythonFunc("manager", "main", NULL);
    
    return res;
}


