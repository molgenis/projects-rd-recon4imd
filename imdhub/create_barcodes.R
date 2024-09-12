
library(baRcodeR)

example_labels <- uniqID_maker(user = FALSE, string = "P", level = 1:20)

participant_data$participant_id <- "PJHVBB"
participant_data <- data.frame(
  specimen_code = c(
    "U", "Ua1", "Ua2", "Ua3",
    "P", "Pa1", "Pa2", "Pa3",
    "BG", "Pax", "FP", "S",
    "v1-Ua1", "v1-Ua2", "v1-Ua3",
    "v2-Ua1", "v2-Ua2", "v2-Ua3"
  )
)

participant_data$label <- paste(
  participant_data$participant_id,
  participant_data$specimen_code,
  sep = "-"
)


custom_create_PDF(
  name = "test",
  Labels = participant_data$label,
  type = "linear",
  Fsz = 11,
  numrow = 18,
  numcol = 4,
  page_width = 8.3,
  page_height = 11.7,
  label_width = 1.9,
  label_height = 0.59,
)