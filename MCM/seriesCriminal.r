library(gdistance)
library(ggplot2)
library(ggmap)
library(raster)
library(leaflet)
library(d3heatmap)

ggplot(aes(x=-LON, y=LAT), data=location) +
  geom_blank() + coord_map("mercator") +geom_point()+xlim(-3,-1)+ylim(53.3,54)
#ggplot+(map)+heatmap
LONseries = -location$LON
LATseries = location$LAT


density = matrix(rep(0,400),20)
for (i in 1:20) {
  for (j in 1:20){
    LON = seq(-3,-1,0.1)[i]
    LAT = seq(53.3,54,0.035)[j]
    density[i,j] = mean(1/((LON-LONseries)^2+(LAT-LATseries)^2))
  }
}
heatmap(density)

p <- ggplot(density, aes(variable, Name)) + geom_tile(aes(fill = rescale)) + scale_fill_gradient(low = "white",
                                                                                                   +     high = "steelblue")
d3heatmap(density,  dendrogram = "none",color = scales::col_quantile("Blues", NULL, 10))

d3heatmap(density,  dendrogram = "none",color = c("#9e0142",
  "#d53e4f",
  "#f46d43",
  "#fdae61",
  "#fee08b",
  "#ffffbf",
  "#e6f598",
  "#abdda4",
  "#66c2a5",
  "#3288bd",
  ))

leaflet() %>% addTiles() %>%
  addMarkers(data = location, lat = ~ LAT, lng = ~ -LON)

