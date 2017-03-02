#!/bin/sh

for name in blast ssaha bwa shrimp lifemapper snpexp bwa-gatk
do
	echo "generating $name..."
        makeflow_viz $name/$name.mf --display dot --dot-no-labels > $name/$name.dot
	dot -Tpng -Gsize=10,10\! -Gdpi=100 -Gratio=fill $name/$name.dot > $name/$name.png
	dot -Tpdf -Gsize=10,10\! -Gdpi=100 -Gratio=fill $name/$name.dot > $name/$name.pdf
done

