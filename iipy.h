/* Copyright (C) 2012-2013 Teodor Spæren <teodor_spaeren@lavabit.com>
 * Licensed under the 2-clause BSD license, see LICENSE. */
#include <Python.h>
#include <dirent.h>


#ifndef IIPY_H_INCLUDED
#define IIPY_H_INCLUDED

/* General functions */
int Load_Python(char *host, char nick[], char path[]);
int Load_PythonFunc(char* sModule, char* sFunc, PyObject *args);
int iipy_LoadEvent(PyObject *info);

/* All in one Environment function */
int iipy_SetEnv(char *host, char nick[], char path[]);

/* Event functions */
int iipy_ReceiveEvent(char *channel, char *time, char *msg);


#endif