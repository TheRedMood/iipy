/* Copyright (C) 2012-2013 Teodor Spæren <teodor_spaeren@lavabit.com>
 * Licensed under the 2-clause BSD license, see LICENSE. */
#include <Python.h>
#include <dirent.h>


#ifndef IIPY_H_INCLUDED
#define IIPY_H_INCLUDED

/* General functions */
int Load_Python(void);
int Load_PythonFunc(char* sModule, char* sFunc, PyObject *args);
int iipy_LoadEvent(PyObject *info);

/* Environment functions */
int iipy_SetVar(char *name, void *value, char type);

// Specific variables
int iipy_SetHost(char *host);
int iipy_SetNick(char nick[]);
int iipy_SetPath(char path[]);

/* All in one Environment function */
int iipy_SetEnv(char *host, char nick[], char path[]);

/* Event functions */
int iipy_SpokeEvent(char *channel, char *msg);

#endif
