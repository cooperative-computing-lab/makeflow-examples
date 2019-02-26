#!/bin/sh

EXAMPLES="blast ssaha bwa shrimp lifemapper snpexp bwa-gatk hecil shakespeare"

for name in $EXAMPLES
do
	echo "generating $name..."
        makeflow_viz $name/image.mf --display dot --dot-no-labels > $name/image.dot
	dot -Tpng -Gsize=10,10\! -Gdpi=100 -Gratio=fill $name/image.dot > $name/image.png
	dot -Tpdf -Gsize=10,10\! -Gdpi=100 -Gratio=fill $name/image.dot > $name/image.pdf
done

montage -geometry 256x256 -tile $(echo $EXAMPLES | wc -w)x1 */image.png banner.png
