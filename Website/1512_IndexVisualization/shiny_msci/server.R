
# This is the server logic for a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
#
library(shiny)
library(dygraphs)
library(dplyr)
library(xts)

shinyServer(function(input, output) {
  
  world <- read.csv("world.csv") 
  world$msci <- as.numeric(gsub(",","",world$msci)) 
  acwi <- read.csv("acwi.csv") 
  acwi$msci <- as.numeric(gsub(",","",acwi$msci)) 
  
  datasetInput <- reactive({
    switch(input$dataset,
           "world" = world,
           "acwi" = acwi)
  })
  
  output$mscigraph <- renderDygraph({
      dataset <- datasetInput()
      xts(dataset$msci, as.Date(dataset$date, format = "%m/%d/%Y")) %>%
      dygraph() %>%
      dyAxis("x", drawGrid = FALSE) %>%
      dyRangeSelector(height=20)
  })
  
})


