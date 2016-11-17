
FIGURES=lifemapper/lifemapper.png ssaha/ssaha.png snpexp/snpexp.png bwa-gatk/bwa-gatk.png

all: ${FIGURES}

lifemapper/lifemapper.mf: lifemapper/make_lifemapper
	lifemapper/make_lifemapper 20 7 > lifemapper/lifemapper.mf

ssaha/ssaha.mf: ssaha/make_ssaha
	ssaha/make_ssaha > ssaha/ssaha.mf

bwa/bwa.mf: bwa/make_bwa
	bwa/make_bwa > bwa/bwa.mf

%.png: %.dot
	/usr/bin/time dot -Tpng -Gsize=10,10\! -Gdpi=100 -Gratio=fill $< > $@

%.dot: %.mf
	makeflow_viz $< --display dot --dot-no-labels > $@
