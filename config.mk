# Customize to fit your system

# paths
PREFIX	  = /usr/local
BINDIR	  = ${PREFIX}/bin
MANDIR	  = ${PREFIX}/share/man
MAN1DIR	 = ${MANDIR}/man1
DOCDIR	  = ${PREFIX}/share/doc/ii

# Set the following to install to a different root
DESTDIR	 =

INCDIR	  = ${PREFIX}/include
LIBDIR	  = ${PREFIX}/lib
VERSION	 = 1.7

# includes and libs
INCLUDES	= -I. -I${INCDIR} -I/usr/include
LIBS		= -L${LIBDIR} -L/usr/lib -lc
# uncomment and comment other variables for compiling on Solaris
#LIBS = -L${LIBDIR} -L/usr/lib -lc -lsocket -lnsl
#CFLAGS	  = -g ${INCLUDES} -DVERSION=\"${VERSION}\"

# compiler
CC		  = cc
CFLAGS	  = -g -O0 -W -Wall ${INCLUDES} -DVERSION=\"${VERSION}\" `python3.2-config --cflags`
LDFLAGS	 = ${LIBS} `python3.2-config --ldflags`
