#!/bin/sh
# Ham veriyi Olist'in resmî deposundan, sabit bir sürümden indirir. Veri bu depoya kopyalanmaz.
set -e
rm -rf veri
git clone -q https://github.com/olist/work-at-olist-data veri
git -C veri checkout -q d9e4980
echo "Veri hazır: veri/datasets"
