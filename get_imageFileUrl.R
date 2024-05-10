# BEM 1/9/24
# Purpose: downloads dhp meta-data

# R version 4.1.2
# neonUtilities version 2.4.1
#install.packages("neonUtilities")
library(neonUtilities)

xx <- neonUtilities::loadByProduct(dpID = "DP1.10017.001", site = "PUUM")
Sys.time() # [1] "2024-01-09 09:50:29 HST"
xx <- xx[['dhp_perimagefile']]

write.csv(xx, 'dhp_perimagefile.csv', row.names = F)