
FIGURES=lifemapper/lifemapper.png ssaha/ssaha.png snpexp/snpexp.png

all: ${FIGURES}

lifemapper/lifemapper.mf: lifemapper/make_lifemapper
	lifemapper/make_lifemapper 20 7 > lifemapper/lifemapper.mf

ssaha/ssaha.mf: ssaha/make_ssaha
	ssaha/make_ssaha > ssaha/ssaha.mf

%.png: %.dot
	dot -Tpng $< > $@

%.dot: %.mf
	makeflow_viz $< --display dot --dot-no-labels > $@
