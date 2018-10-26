TEMPLATE = app
CONFIG += console
CONFIG -= app_bundle
CONFIG -= qt
TARGET = signon-storage-perm

INCLUDEPATH +=  ../src ../lib
SOURCES += signon-storage-perm.c

target.path = $${INSTALL_PREFIX}/usr/libexec

INSTALLS += target
