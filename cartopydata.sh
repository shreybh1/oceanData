CARTOPY_DIR=/usr/local/cartopy-data
NE_PHYSICAL=${CARTOPY_DIR}/shapefiles/natural_earth/physical
mkdir -p ${NE_PHYSICAL}
wget https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/physical/ne_10m_coastline.zip -P ${CARTOPY_DIR}
unzip ${CARTOPY_DIR}/ne_10m_coastline.zip -d  ${NE_PHYSICAL}
rm ${CARTOPY_DIR}/*.zip
