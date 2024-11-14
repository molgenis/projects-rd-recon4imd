#'////////////////////////////////////////////////////////////////////////////
#' FILE: create_gantt.R
#' AUTHOR: David Ruvolo
#' CREATED: 2024-10-09
#' MODIFIED: 2024-10-09
#' PURPOSE: Create gantt chart
#' STATUS: in.progress
#' PACKAGES: ggplot2, tribble, dplyr
#' COMMENTS: NA
#'////////////////////////////////////////////////////////////////////////////

# install
#' install.packages("dplyr")
#' install.packages("ggplot2")
#' install.packages("tibble")
#' install.packages("httpgd")

library(ggplot2)
library(tidyr)
library(dplyr)
library(grid)

gantt_data <- tibble::tribble(
  ~category, ~aim, ~date_start, ~date_end, ~completed,
  "Setup", "1-3", "2024-01-01", "2024-03-01", 1,
  "Data", "4-5", "2024-03-01", "2024-12-31", 1.1,
  "Data", "7", "2024-12-01", "2025-03-01", 0.5,
  "Development", "6", "2024-04-01", "2024-07-01", 1,
  "Development", "6", "2024-12-01", "2025-03-01", 0.5,
  "Onboarding", "8", "2024-11-01", "2025-07-01", 0.5,
  "Management", "4", "2024-02-01", "2025-12-31", 1.1,
)

gantt_data_tidy <- gantt_data %>%
  mutate(
    date_start = as.Date(date_start),
    date_end = as.Date(date_end)
  ) %>%
  gather(key =  date_type, value = date, -category, -aim, -completed) %>%
  mutate(
    category = factor(
      x = category,
      levels = c(
        "Management",
        "Onboarding",
        "Development",
        "Data",
        "Setup"
      )
    ),
    completed = factor(x = completed, levels = c(0.5, 1, 1.1))
  )


# create chart
chart <- ggplot() +
  geom_line(
    data = gantt_data_tidy,
    mapping = aes(x = category, y = date, group = category),
    color = "#5FA8D3",
    size = 18
  ) +
  scale_y_date(
    date_breaks = "3 months",
    date_labels = "%b %Y",
    limits = c(as.Date("2024-01-01"), as.Date("2026-01-01")),
    expand = c(0, 0)
  ) +
  coord_flip() +
  geom_hline(yintercept = Sys.Date(), colour = "black", linetype = "dashed") +
  labs(
    x = NULL,
    y = NULL,
    title = "RECON4IMD: IMDHUB",
    subtitle = "Timeline to development the IMDHub and ongoing support"
  ) +
  theme_classic() +
  theme(
    # legend.position = "none",
    plot.margin = unit(rep(1, 4), "cm"),
    axis.ticks.y = element_blank(),
    plot.title = element_text(size = 9, face = "bold"),
    plot.subtitle = element_text(size = 12, face = "plain")
  )

ggsave(
  filename = "files/imdhub_gantt.png",
  plot = chart,
  width = 10.3,
  height = 5.14,
  units = "in"
)