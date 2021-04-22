# -------------------------------------
# Makefile for Library Installation
# -------------------------------------

cur = $PWD
dpath ?= $(cur)$"/dist"
msg1 ?= "wheel build done"

install:
	echo Building wheel for the package
	python setup.py bdist_wheel
	if [ -d $(dpath) ]; then \
  		echo $(msg1); \
  		cd $(dpath); \
    	pip3 install opti_lib-1.0.0-py3-none-any.whl; \
    fi

clean:
	pip3 uninstall opti_lib
	if [ -d $(dpath) ]; then \
        sudo rm -rf $(dpath);\
    fi
	path = $(cur)$"/build"
	if [ -d $(path) ]; then \
        sudo rm -rf $dpath;\
    fi

