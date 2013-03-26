/* Copyright (C) 2012-2013 Teodor Spæren <teodor_spaeren@lavabit.com>
 * Licensed under the 2-clause BSD license, see LICENSE. */
#include <Python.h>
#include <dirent.h>


#ifndef IIPY_H_INCLUDED
#define IIPY_H_INCLUDED

int Load_Python(void);
int Load_PythonFunc(char* sModule, char* sFunc, PyObject *args);
int iipy_LoadEvent(PyObject *info);

/* Event functions */
int iipy_SpokeEvent(char* channel, char* msg);
#endif
