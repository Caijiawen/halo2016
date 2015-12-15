
# This is the user-interface definition of a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
#

library(dygraphs)
library(shiny)

shinyUI(fluidPage(
  titlePanel("MSCI Index"),
  
  sidebarLayout(
    sidebarPanel(
      selectInput("dataset", "Choose a dataset:", 
                  choices = c("world", "acwi"))
    ),
    
  
    mainPanel(
        dygraphOutput("mscigraph"))
  
  )
  ))