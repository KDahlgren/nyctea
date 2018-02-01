# based on https://github.com/KDahlgren/pyLDFI/blob/master/Makefile

all: deps

deps: get-submodules iapyx

clean:
	rm -r lib/iapyx

cleaniapyx:
	rm -r lib/iapyx

iapyx:
	cd lib/iapyx ; python setup.py ;

get-submodules:
	git submodule init
	git submodule update
