#!/usr/bin/env Rscript
# Frozen reference for sp.sqreg vs R quantreg::rq (simultaneous quantile
# regression at multiple tau). Both minimize the same pinball loss with the
# same Frisch-Newton interior point solver, so coefficients and SEs match
# quantreg::summary.rq's "nid" default to machine precision.
suppressPackageStartupMessages({library(quantreg); library(jsonlite)})
df <- read.csv("tests/reference_parity/_fixtures/sqreg_data.csv")
extract <- function(tau) {
  fit <- rq(y ~ x1 + x2 + x3, tau = tau, data = df, method = "br")
  as.list(coef(fit))
}
out <- list(
  tau_025 = extract(0.25),
  tau_050 = extract(0.50),
  tau_075 = extract(0.75),
  provenance = list(
    r_version = R.version.string,
    quantreg_version = as.character(packageVersion("quantreg")),
    generated_by = "tests/reference_parity/_generate_sqreg_R.R"
  )
)
writeLines(toJSON(out, auto_unbox = TRUE, digits = 16, pretty = TRUE),
           "tests/reference_parity/_fixtures/sqreg_R.json")
cat("wrote sqreg_R.json\n")
