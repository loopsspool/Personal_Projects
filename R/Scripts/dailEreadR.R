# dailEreadR.R
# reads dailE list and returns graphs and data based on list
# Ethan Jones, 2/12/2019 (try to find actual day you started working on it, though)
# ~69.25 hours


#################################   IMPORTANT   #################################
# This entire script is based off of the Extra Info sheet being in chronological order
# Rows in the dailE sheet can be swapped, BUT KEEP THE EXTRA INFO SHEET CHRONOLOGICALLY ORDERED
# Also new rows are only counted if they're added to dailE info, since dailE trimming is based off that sheet
# Also don't add new things on days that aren't real LOL


######################################   GLOBALS   ######################################
suppressMessages(library(tidyverse))
suppressMessages(library(readxl))
suppressMessages(library(tibble))
suppressMessages(library(dplyr))
suppressMessages(library(lubridate))
#browseVignettes(package = "readxl")

# Takes out ANSI escape codes (I assume for color for columns) that was causing printing to look bad
options(crayon.enabled = FALSE)

# TODO: Assess if OG tibble needs real days in it or not 
# OG_dailE does have blank rows removed
OG_dailE <- read_excel("C:\\Users\\ejone\\OneDrive\\Desktop\\dailE.xlsm", sheet = "List")
dailE <- read_excel("C:\\Users\\ejone\\OneDrive\\Desktop\\dailE.xlsm", sheet = "List")
dailE_info <- read_excel("C:\\Users\\ejone\\OneDrive\\Desktop\\dailE.xlsm", sheet = "Extra Info")

command_arg_dates <- c()
start_date <- 0
end_date <- 0
blank_dates <- c()
blank_dates_within_range <- c()

amount_of_things_to_do_at_date <- list()
amount_of_rows_at_date <- list()
amount_of_dates_tracked <- list()
amount_of_dates_trackers_were_done <- list()
amount_of_days_tracker_included <- list()
amount_of_days_things_included <- list()
amount_of_times_words_mentioned <- list()
amount_of_real_days <- 0
amount_of_potential_days <- 0
amount_of_days_in_range <-c()

date_when_things_were_added <- list()
date_when_tracker_quantification_started <- list()

numerical_tracker_vectors <- list()

totals_from_all_rows <- list()
totals_of_times_trackers_done <- list()
totals_of_times_things_done <- list()
totals_from_trackers <- list()
total_things_completed_daily <- list()
# TODO: Change at to for here for the below, if this is refrencing things done in date ranges
total_of_things_done_at_date <- list()

averages_from_trackers <- list()
average_things_done_in_range_percentage <- list()
# TODO: Take out daily in the name below?
average_things_done_in_range_daily_number <- list()
average_overall_things_done_per_day_percentage <- 0
average_overall_things_done_per_day_number <- 0
average_amount_of_things_to_do <- 0

percentage_of_days_trackers_completed <- list()
percentage_of_days_things_completed <- list()
percentage_of_days_completed <- 0

sum_of_all_rows <- 0
sum_of_things_to_do <- 0
sum_of_trackers <- 0
sum_of_all_things_done <- 0

max_of_trackers <- list()
min_of_trackers <- list()

words_to_be_searched <- c("Bryce", "Rachel", "autumn","fortnite", "cloud", "sunset", "lol", ":)", "!", "fuck", "shit")


######################################   HIGH IMPORTANCE TODOS   ######################################
# TODO: Seems a bit bogged... avoid all loops and try to use apply functions. Look into possible iterator
  # Happened in loops involved with averages, seems like
  # Slower with bigger amount of days to deal with
  # Use print statement to find before/after when function operates quickly
# TODO: Make sure zeros don't count as a thing done. 
  # With this, determine whether to include in sheet or just have nas count as zeros dealing with trackers in this script
# TODO: Adjust average amount of things to do to bias the bigger numbers more (proper weighted(?) average)
# TODO: Change not sober to an extra credit
  # Count if blank, not if marked
  # Also EC: fail(?), face something, take a risk
# TODO: Sort totals and averages output to order in dailE list, not chronological. Prolly via OG_dailE
# TODO: Create function to be used with sapply to easily cat all vector stuff and be more in line with R philosophy
# TODO: Make it so quality of day /10 is ALWAYS only averaged for days counted
# TODO: Exclude quality of day tracker from being totalled
# TODO: Have default command line run most recent real day or present day running program? Have parameters? Which default?
# TODO: Adhere to Google Style R rules
# TODO: Chronologically order dailE_info so it isn't necessary that its chronological on the excel spreadsheet
  # Maybe notify user which row is out of order

######################################   MED IMPORTANCE TODOS   ######################################
# TODO: Have like an end_day_index to be called easily on amount_of_things_to_do_at_date, etc
# TODO: Create a projected number of steps done towards improving yourself 
  # rough average of how many times you ACTUALLY do things for each day you completed it?
  # Row in dailE info of amount of times prolly actually do thing in a day?
# TODO: Unify date names in lists stored as numerics or characters, prolly numerics
# TODO: Figure out how you wanna deal with wake up early row (def with datetimes)
# TODO: Find % of days 100% done for
# TODO: How many zero days (of trackers? Everything?)
# TODO: Prediction incorectness ratio
# TODO: Maybe have things that adds to tracker totals if its a not real day but still has data. Default boolean somewhere
  # Trackers only? Include to-dos too? Or?
# TODO: have date quantification started also be for text answers, when started writing actual responses, not just x
# TODO: See if amount of words typed for the day corresponds with quality of day

######################################   LOW IMPORTANCE TODOS   ######################################
# TODO: Create column in dailE info excel for min/hr tracker time type. Have a min, hr, and normal time vector?
# TODO: Longest streak of each row and date range 
  # boolean variable for if non-real days kill streak or not
# TODO: Max of numerical tracker rows (min too?)
# TODO: Weekday analysis (better quality of day, more things done on certain days, higher trackers on certain days, etc)
# TODO: Create report of color of days for seasons. Seperate by year
  # If possible also run similarity analysis -- similar hues, brightness, etc
# TODO: Account for plural when answer may only be 1 using cat


###########################################    MISC FUNCTIONS    ###########################################
user_input <- function()
{
  # Reads command line input if any given
  # Parses into a date vector for other functions to use
  command_args <- commandArgs(trailingOnly = TRUE)
  if (length(command_args) > 2)
  {
    stop ("Only up to 2 dates are allowed")
  }
  # TODO(try block here to see if it can convert string to date? If not print proper format)
  command_arg_dates <<- mdy(command_args)
}

error_checker <- function()
{
  # TODO: rename to error_detector?
  # TODO: Add checker for if amount of rows in dailE, stripped of blank rows, does not equal dailE_info rows
  # If not, send message to user that the row will only register if it is recorded in dailE info with necessary column info (date time started, quantification in tracker, etc)
  # But after blank row trimming
  # TODO: Also add checker in dailE_info if tracker has quantification start date, everything has start date, etc
  # Spit out messages explaining whats wrong and what needs to be done
  # Checks for inconsistency in data so program wont operate unless everyhings synced (dailE & dailE_info)
  
  if (nrow(dailE) != nrow(dailE_info))
  {
    cat ("\ndailE rows:", nrow(dailE), "\n")
    cat ("dailE info rows:", nrow(dailE_info), "\n\n")
    
    cat ("There is an inconsistency in your data. 
         This is caused by a row being added to dailE info but not to the dailE sheet.
         Or if the row is listed in both, the names do not match.
         \n")
    
    confirmed_rows <- which (unlist(dailE[, 1]) %in% unlist(dailE_info[,1]))
    problem_rows <- unlist(dailE_info[-confirmed_rows, 1])
    cat ("Problem row(s) as listed in dailE info:", "\n")
    sapply(problem_rows, function (x) cat (x, "\n"))
    
    quit()
  }
  
}

graph <- function()
{
  # TODO: See dailE colors of seasons
  # TODO: Scatter of trackers & quality of day
  # TODO: Scatter of things done and quality of day
  
  # TODO: See why not printing. Also spread out days on graph so can visualize time in between
  hist(as.numeric(amount_of_rows_at_date))
}


###########################################    CONVERTER  FUNCTIONS    ###########################################
convert_dates_from_excel_to_R <- function()
{
  # Renames columns with R integer dates instead of excel integer dates

  date_vector <- colnames(dailE)
  hyphen_in_first_cell <- FALSE
  
  # Checks if theres a hyphenated cell at the beginning
    # This is cause my column name for the row names was blank, but tidyverse "repairs" the name to ..#
      # This act also gives a terminal log, which I didn't want
        # Since I couldn't find a way to suppress it, I named the column "-" lol
  if (as.character(date_vector[1]) == "-")
  {
    hyphen_in_first_cell <- TRUE
    
    # Takes out first element (/column) bc of headers
    date_vector <- date_vector[-1]
  }
  
  ######################     Actual conversion math     ######################
  
  # Excel saves dates as an integer number of days past 1-0-1900. So 1-1-1900 is 1. Also incorrect assumption of leap year that year.
  # With those two extra days, correct start date of Excel dates would be below
  first_excel_date <- as.Date("1899-12-30")
  R_date_vector <- c()
  
  # Since first_excel_date is an R date object, it is stored as a negative integer representing days before 1970-1-1
    # Then adding amount of days from first_excel_date to the date passed in gives an R integer of days past 1970-1-1
  R_date_vector <- first_excel_date + as.numeric(date_vector)
  
  if (hyphen_in_first_cell)
    R_date_vector <- c("-", R_date_vector)
  
  colnames(dailE) <<- R_date_vector
  
  # Don't need to call convert_dates_from_excel_to_R on dailE_info$'Date Quantification Started' or dailE_info$'Date Added'
  # because they're already Date objects? Maybe R didn't convert the ones in DailE because they're column names?
}

R_date_ints_to_date <- function(date_vec)
{
  class(date_vec) <- "Date"
}

printable_date_from_int <- function(date_int)
{
  # Creates date object from date int
  date <- as_date(date_int)
  # Then can print date representation of date int
  return(as.character(date))
}


###########################################    INITIALIZER FUNCTIONS    ###########################################
initializers <- function()
{
  user_input()
  convert_dates_from_excel_to_R()
  rid_of_empty_days()
  # Start and end date are set after getting rid of the empty days so everything operates according to the 
    # dailE tibble after it was modified to only contain days that have real data
  set_when_things_were_added()
  set_start_and_end_date()
  
  # Removes blank rows used for natural spacing
  # Not in resize_dataframes because it needs to be done before reorder_dataframes
  dailE <<- remove_na_rows(dailE)
  OG_dailE <<- remove_na_rows(OG_dailE)
  
  reorder_dataframes()
  resize_dataframes()
  error_checker()
  # initialize_totals must be after set_start_and_end_date because it has a dependency from it (end_date)
  initialize_totals()
  initialize_averages()
}

initialize_totals <- function(start, end)
{
  set_total_things_at_date()
}

initialize_averages <- function()
{
  gets_how_many_days_in_between_date_ranges()
}


###########################################    ORGANIZING FUNCTIONS    ###########################################
reorder_dataframes <- function()
{
  dailE_info_index_from_dailE <- match(unlist(dailE[, 1]), unlist(dailE_info$'Row Name'))
  dailE <<- arrange(dailE, dailE_info_index_from_dailE)
}

resize_dataframes <- function()
{
  # Shrinks tibbles to start & end date so no need for indexing within functions using the tibbles
  
  start_index <- which (colnames(dailE) == as.numeric(start_date))
  end_index <- which (colnames(dailE) == as.numeric(end_date))
  # Date range of only days actually completed from start_date to end_date
  date_range <- colnames(dailE)[start_index:end_index]
  
  # Gets lall rows that were added before (or equal to) the end date
  # Since list is cumulative, will include all rows created prior to any specified date
  dailE_info_row_end_index <- which(as_date(dailE_info$'Date Added') <= as_date(end_date))
  # Actually gets last row in list to chop off all below (added after end date)
  dailE_info_row_end_index <- dailE_info_row_end_index[length(dailE_info_row_end_index)]
  rows_to_keep <- 1:dailE_info_row_end_index
  # Trims dailE_info to only rows added at date
  dailE_info <<- dailE_info[rows_to_keep,]
  
  # Assigns properly dated rows for end date (so there isn't a bunch of blank rows that haven't been created yet at the time of end_date)
  # rows_to_keep same as dailE_info thanks to reorder_dataframes
  dailE <<- dailE[rows_to_keep, date_range]
  # Adds back Row names to beginning of dailE tibble
  dailE <<- add_column(dailE, "Row Names" = dailE_info$'Row Name'[rows_to_keep], .before = 1)
  
  # Sets amount of days in range
  # Minus 1 due to row name column
  amount_of_real_days <<- ncol(dailE) - 1
}

remove_na_rows <- function(df)
{
  na_vector <- which(is.na(df[, 1]))
  return(df[-na_vector, ])
}

rid_of_empty_days <- function()
{
  real_day_row_index <- get_row_index_from_name('Real Day Number')
  not_real_day_column_indices <- which(is.na(dailE[real_day_row_index,]))
  blank_dates <<- colnames(dailE)[not_real_day_column_indices]
  class(blank_dates) <<- 'Date'
  dailE <<- dailE[, -not_real_day_column_indices]
}

delete_days_before_range <- function(row_list)
{
  i <- 1
  # i + 1 less than start date so it only takes off dates that occur completely irrelevant to start date
  # In other words, if the start date is smack in the middle of two dates when new things were added
  # You'll need to retain the first nearest date before the start date to know how many things there were at the start date
  # And since they're summed from dates prior, all dates preceeding this are irrelevant
  # Also, just as a note the order of these conditionals are important as the first stops an out-of-index error for the second
  while ( (i < (length(row_list))) & as_date(names(row_list[i + 1])) <= start_date )
  {
    i <- i + 1
  }
  # Trims row_list of amount things to do from relevant start to last before end date
  row_list <- row_list[i:length(row_list)]
  
  # If the first element is before the start date (things were added before the start date), make that date the start date
  # This is important for later on referencing this list
  # An error will be thrown searching for the added thing date index if its before the start date since it was trimmed off 
  # (because it was before the start date)
  if (as_date(names(row_list[1])) < start_date)
    names(row_list)[1] <- printable_date_from_int(as.numeric(start_date))
  
  return (row_list)
}


###########################################    SETTER FUNCTIONS    ###########################################
# TODO(assess after usage if you want to keep buffer in between start & end date the same)
  # eg if you're looking for a week of data but both dates are not done, returned dates still give a week of data
  # must use difference of indices in list of ALL dates (even those not done), then apply that difference on list of real dates
    # or lubridate intervals or something of the sort
set_start_and_end_date <- function()
{
  first_dailE_date <- colnames(dailE)[2]
  last_dailE_date <- colnames(dailE)[ncol(dailE)]
  class(first_dailE_date) <- 'Date'
  class(last_dailE_date) <- 'Date'
  
  # Strictly larger than 1 necessarily must be 2 since an error is returned at anything larger than 2 command line arguments
  if (length(command_arg_dates) > 1)
  {
    # Sorts dates so earliest is always first
    command_arg_dates <<- sort(command_arg_dates)
    
    # If specified start & end date are both before dailE starting date kill script
    if (command_arg_dates[1] < first_dailE_date
        && command_arg_dates[2] < first_dailE_date)
    {
      cat ("\n The two dates entered are before dailE started (1-1-2018). Please enter dates on or after this date.\n")
      quit(save = "no")
    }
    # If specified start & end date are both after dailE end date kill script
    if (command_arg_dates[1] > last_dailE_date
        && command_arg_dates[2] > last_dailE_date)
    {
      cat ("\n The two dates entered are after the last real dailE date -- currently",
           printable_date_from_int(last_dailE_date),
           ". Please enter dates on or before this date.\n")
      quit(save = "no")
    }
    # If specified start & end date are the same and on a non-real day kill script
    if (command_arg_dates[1] == command_arg_dates[2]
        && command_arg_dates[1] %in% blank_dates
        && command_arg_dates[2] %in% blank_dates)
    {
      cat ("\nThe two dates were the same and a on date that was not recorded. 
           The program has been stopped, please re enter command line call with different dates.\n")
      quit(save = "no")
    }

    # checks for valid end date input
    if (command_arg_dates[2] < first_dailE_date)
    {
      end_date <<- first_dailE_date
      cat("\nThe end date input",
          printable_date_from_int(command_arg_dates[2]), 
          "is before the first start date of", 
          printable_date_from_int(first_dailE_date), 
          ". Date has been changed to be the first start date.\n")
    }
    else if (command_arg_dates[2] > last_dailE_date)
    {
      end_date <<- last_dailE_date
      cat("\nThe end date input",
          printable_date_from_int(command_arg_dates[2]), 
          "is after the last date of", 
          printable_date_from_int(last_dailE_date), 
          ". Date has been changed to be the last date.\n")
    }
    else if (as_date(command_arg_dates[2]) %in% blank_dates)
    {
      end_date <<- get_next_closest_day(command_arg_dates[2])
      cat('\nThe end date input', 
          printable_date_from_int(command_arg_dates[2]), 
          'was on a day not completed. The end date has been moved to the next closest forward completed day --', 
          printable_date_from_int(end_date), "\n")
    }
    else
    {
      end_date <<- command_arg_dates[2]
    }
  }
  
  if (length(command_arg_dates) >= 1)
  {
    if (command_arg_dates[1] < first_dailE_date)
    {
      start_date <<- first_dailE_date
      cat("\nThe start date input",
          printable_date_from_int(command_arg_dates[1]), 
          "is before the first start date of", 
          printable_date_from_int(first_dailE_date), 
          ". Date has been changed to be the first start date.\n")
    }
    else if (command_arg_dates[1] > last_dailE_date)
    {
      start_date <<- last_dailE_date
      cat("\nThe start date input",
          printable_date_from_int(command_arg_dates[1]), 
          "is after the last date of", 
          printable_date_from_int(last_dailE_date), 
          ". Date has been changed to be the last date.\n")
    }
    else if (as_date(command_arg_dates[1]) %in% blank_dates)
    {
      start_date <<- get_next_closest_day(command_arg_dates[1])
      cat('\nThe start date input', 
          printable_date_from_int(command_arg_dates[1]), 
          'was on a day not completed. The start date has been moved to the next closest forward completed day --', 
          printable_date_from_int(start_date), "\n")
    }
    else
    {
      start_date <<- command_arg_dates[1]
    }
    
    if (length(command_arg_dates) == 1)
    {
      end_date <<- last_dailE_date
    }
  }
  
  if (length(command_arg_dates) == 0)
  {
    start_date <<- first_dailE_date
    end_date <<- last_dailE_date
  }
}

set_when_things_were_added <- function()
{
  row_name <- dailE_info$'Row Name'
  date_added <- dailE_info$'Date Added'
  
  # TODO: R-ify
  for (i in 1:length(row_name))
  {
    date_when_things_were_added[row_name[i]] <<- toString(date_added[i])
  }
}

set_total_things_at_date <- function()
{
  # TODO: R-ify
  # Keeps track of the total amount of things to do (excluding trackers) at dates new things were added. 
  # Stored as 'Date Key' : total in amount_of_things_to_do_at_date
  
  row_name <- dailE_info$'Row Name'
  date_added <- dailE_info$'Date Added'
  tracker <- dailE_info$'Numerical Tracker?'
  non_to_dos <- dailE_info$"Shouldn't be counted in to-dos"
  not_to_count <- dailE_info$"Shouldn't be counted anywhere"
  
  for (i in 1:length(row_name))
  {
    # Totals of all rows at dates
    if (!((toString(date_added[i]) %in% names(amount_of_rows_at_date))) & is.na(not_to_count[i]))
    {
      # Concatenate it to list with a value of 1 if it's not already denoted
      amount_of_rows_at_date[toString(date_added[i])] <<- 1
    }
    # Adds to total at date IF it is a tracker row
    # not_to_count includes tracking info such as column number, real day number, special comments, daily hex color, etc
    else if (is.na(not_to_count[i]))
    {
      # Otherwise just add 1
      amount_of_rows_at_date[toString(date_added[i])] <<- as.numeric(amount_of_rows_at_date[toString(date_added[i])]) + 1
    }
    
    # Just when things to do (so excludes trackers) were added at what date 
    if (is.na(non_to_dos[i]))
    {
      # if date at iteration is not in list
      if (!(toString(date_added[i]) %in% names(amount_of_things_to_do_at_date)))
      {
        # Concatenate it to list with a value of 1
        amount_of_things_to_do_at_date[toString(date_added[i])] <<- 1
      }
      else
      {
        # Otherwise just add 1
        amount_of_things_to_do_at_date[toString(date_added[i])] <<- as.numeric(amount_of_things_to_do_at_date[toString(date_added[i])]) + 1
      }
    }
    
    # Just trackers
    if (!is.na(tracker[i]))
      sum_of_trackers <<- sum_of_trackers + 1
  }
  
  # Sums up amount of things to do so each future date contains sum of things of past dates
  amount_of_things_to_do_at_date <<- sum_up_all_prior_rows(amount_of_things_to_do_at_date)
  amount_of_rows_at_date <<- sum_up_all_prior_rows(amount_of_rows_at_date)
  
  # Gets rid of dates before specified start in command line date range
  amount_of_things_to_do_at_date <<- delete_days_before_range(amount_of_things_to_do_at_date)
  amount_of_rows_at_date <<- delete_days_before_range(amount_of_rows_at_date)
  
  # Sets globals
  sum_of_things_to_do <<- as.numeric(unlist(amount_of_things_to_do_at_date[length(amount_of_things_to_do_at_date)]))
  sum_of_all_rows <<- as.numeric(amount_of_rows_at_date[length(amount_of_rows_at_date)])
}


###########################################    GETTER FUNCTIONS    ###########################################
get_row_index_from_name <- function(row_str, df = dailE)
{
  # TODO: Reconsider how this is written
  row_names <- df[, 1]
  return(which(row_names == row_str))
}

get_column_index_from_name <- function(name, df)
{
  indices <- which(colnames(df) %in% name)
  return(indices)
}

get_last_col_in_row <- function(row_str)
{
  row_index <- get_row_index_from_name(row_str)
  row_data <- dailE[row_index,]
  not_nas_in_row <- which(!is.na(row_data))
  
  # return last element
  return(not_nas_in_row[length(not_nas_in_row)])
}

get_next_closest_day <- function(fake_date)
{
  real_day_dates <- colnames(dailE)
  class(real_day_dates) <- 'Date'
  real_days_less_than_command_line <- real_day_dates < fake_date
  real_days_less_than_command_line_indices <- which(real_days_less_than_command_line)
  closest_real_day_index <- real_days_less_than_command_line_indices[length(real_days_less_than_command_line_indices)] + 1
  return(real_day_dates[closest_real_day_index])
}

get_all_occurances_of_words <- function(words)
{
  # TODO: Sort by descending order
  amount_of_times_words_mentioned[words] <<- sapply(words, get_occurances_of_single_word)
}

get_occurances_of_single_word <- function(word)
{
  return(length(grep(word, unlist(dailE), ignore.case = T)))
}


# DATES
gets_how_many_days_in_between_date_ranges <- function()
{
  # TODO: R-ify if possible
  i <- 1
  
  while (i <= length(names(amount_of_things_to_do_at_date)))
  {
    # Simple arithmetic doesn't work because you should only count real days
    # So subtraction of column indices will work (thats what the get_days_in_between function does)
    
    if (i == length(names(amount_of_things_to_do_at_date)))
    {
      # + 1 here to make date range inclusive of range start date
      in_between_days <- get_days_in_between(names(amount_of_things_to_do_at_date)[i], end_date, dailE) + 1
      amount_of_days_in_range <<- c(amount_of_days_in_range, in_between_days)
      break
    }
    
    # + 1 not needed here because this finds the range between one range start date and the NEXT range start date (not the day before)
    # So the range already includes an extra day, making it inclusive
    in_between_days <- get_days_in_between(names(amount_of_things_to_do_at_date)[i], names(amount_of_things_to_do_at_date)[i + 1], dailE)
    amount_of_days_in_range <<- c(amount_of_days_in_range, in_between_days)
    
    i <- i + 1
  }
}

get_amount_of_days_between_thing_start_and_end_date <- function(indices)
{
  # Gets starting date
  row_names <- names(totals_from_all_rows[indices])
  row_indices <- which (names(date_when_things_were_added) %in% row_names)
  row_start_dates <- date_when_things_were_added[row_indices]
  # else {x <- x} needed since returning to a new list, otherwise if not replacing element value would be NA
  adjusted_start_dates <- sapply (row_start_dates, function (x) if (x < start_date) {x <- start_date} else {x <- as_date(x)})
  
  # Finding total amount of days row has been present
  amount_of_days_included <- list()
  amount_of_days_included[names(adjusted_start_dates)] <- sapply(as_date(as.numeric(adjusted_start_dates)), get_days_in_between, big_date = as_date(end_date), df = dailE)
  # +1 to make inclusive, since get_days_in_between counts days IN BETWEEN the two dates
  amount_of_days_included[names(adjusted_start_dates)] <- as.numeric(amount_of_days_included) + 1
  
  return (amount_of_days_included)
}

get_days_in_between <- function(small_date, big_date, df)
{
  return (get_column_index_from_name(ymd(big_date), df) - get_column_index_from_name(ymd(small_date), df))
}


###########################################    MATH FUNCTIONS    ###########################################
calculators <- function()
{
  calculate_totals()
  calculate_averages()
}

# TOTALS
calculate_totals <- function()
{
  
  totals_of_rows_and_columns()
  
  totals_of_numerical_trackers()
  
  totals_things_done_at_date()
  
  get_all_occurances_of_words(words_to_be_searched)
}

# Placed together because they share use of some indices
totals_of_rows_and_columns <- function()
{
  # TODO: Count fill of Todays color
  
  totals_from_all_rows[unlist(dailE[, 1])] <<- rowSums(!is.na(dailE[, -1]) & dailE[, -1] != '-' & dailE[, -1] != 0)
  
  # Get indices & name from dailE_info of rows that aren't technically things to do
  shouldnt_be_included_indices <- which(!is.na(dailE_info$"Shouldn't be counted in to-dos"))
  shouldnt_be_included_names <- dailE_info[shouldnt_be_included_indices, 1]
  
  # Only sum dailE rows that shouldn be included
  sum_of_all_things_done <<- sum(unlist(totals_from_all_rows[-shouldnt_be_included_indices]))
  
  # Remove shouldn't be counted anywhere frm totals_from_all_rows
  shouldnt_be_included_indices <- which(!is.na(dailE_info$"Shouldn't be counted anywhere"))
  shouldnt_be_included_names <- dailE_info[shouldnt_be_included_indices, 1]
  totals_from_all_rows <<- totals_from_all_rows[-shouldnt_be_included_indices]
  
  non_tracker_df <- dailE[-shouldnt_be_included_indices, ]
  # Gets total things completed daily excluding the row names and if the cell value is '-' 
  #(don't need to include 0 because non-tracker rows should never have a numeric value anyways)
  total_things_completed_daily[names(non_tracker_df[, -1])] <<- colSums(!is.na(non_tracker_df[, -1]) & non_tracker_df[, -1] != '-')
}

totals_things_done_at_date <- function()
{
  # Initializes lists
  total_of_things_done_at_date[names(amount_of_things_to_do_at_date)] <<- 0
  
  # TODO: R-ify if possible?
  date_i <- 1
  things_i <- 1
  
  while  (date_i <= amount_of_real_days)
  {
    
    # If the day is the same as a day things were added, change date to next date section for total to be added to
    if (as_date(as.numeric(names(total_things_completed_daily)[date_i])) == as_date(names(amount_of_things_to_do_at_date)[things_i + 1])
        && things_i != length(amount_of_things_to_do_at_date))
    {
      things_i <- things_i + 1
    }

    #cat (printable_date_from_int(as.numeric(names(total_things_completed_daily)[date_i])), printable_date_from_int(names(amount_of_things_to_do_at_date)[things_i]), "\n")
    
    total_of_things_done_at_date[things_i] <<- total_of_things_done_at_date[[things_i]] + total_things_completed_daily[[date_i]]
    
    date_i <- date_i + 1
  }
}

sum_up_all_prior_rows <- function(row_list)
{
  i <- length(row_list)
  while (i > 1)
  {
    row_list[i] <- sum(unlist(row_list[1:i]))
    i <- i - 1
  }
  return (row_list)
}

totals_of_numerical_trackers <- function()
{
  # Gets numerical tracker info from dailE_info and sets global quantification_started
  numerical_tracker_indices <- which(!is.na(dailE_info$"Numerical Tracker?"))
  date_when_tracker_quantification_started[unlist(dailE_info[numerical_tracker_indices, 1])] <<- as_date(dailE_info$"Date Quantification Started"[numerical_tracker_indices])
  
  numerical_tracker_names_to_indices <- list()
  numerical_tracker_names_to_indices[dailE_info$"Row Name"[numerical_tracker_indices]] <- numerical_tracker_indices
  
  # Creates a list of trackers : date the quantification started 
  # To be adapted later based on where this date falls relative to the specified start/end date
  # SO DON'T DELETE lol
  numerical_tracker_names_to_dates <- list()
  numerical_tracker_names_to_dates[names(numerical_tracker_names_to_indices)] <- as_date(dailE_info$"Date Quantification Started"[unlist(numerical_tracker_names_to_indices)])
  
  # Adjust tracker quantification start dates according to possible date range entered in the command line
  # If quantification start dates that are before start date to start date
  quantified_before_start_date_indices <- which (as_date(unlist(numerical_tracker_names_to_dates, use.names = FALSE)) < start_date)
  numerical_tracker_names_to_dates[quantified_before_start_date_indices] <- as.numeric(start_date)
  
  # If the quantification start date is after the specified end date, remove it from being calculated in totals
  quantified_after_end_date_indices <- which (as_date(unlist(numerical_tracker_names_to_dates, use.names = FALSE)) > end_date)
  # And notify the user
  if (length(quantified_after_end_date_indices) > 1)
  {
    cat ("\n")
    sapply (names(numerical_tracker_names_to_dates[quantified_after_end_date_indices]), function (x) {cat ("The tracker row", x, "starts quantification after the end date specified, therefore has been removed from totalling\n")})
  }
  
  # Finds indices of what items should be removed from the numerical_tracker_names_to_indices because quantification starts after end date
  # since not necessarily same order as numerical_tracker_names_to_dates because rows can be shuffled
  quantified_after_end_date_indices_index <- match(names(numerical_tracker_names_to_dates[quantified_after_end_date_indices]), names(numerical_tracker_names_to_indices))
  
  numerical_tracker_names_to_dates[quantified_after_end_date_indices] <- NULL
  numerical_tracker_names_to_indices[quantified_after_end_date_indices_index] <- NULL
  
  # End date
  end_day_index <- get_column_index_from_name(toString(as.numeric(end_date)), dailE)
  
  # Index range of columns
  # Start dates
  column_starts <- sapply(as.vector(unlist(numerical_tracker_names_to_dates)), get_column_index_from_name, dailE)
  
  record_and_sum_numerical_tracker_rows(dailE, numerical_tracker_names_to_indices, column_starts, end_day_index)
}

record_and_sum_numerical_tracker_rows <- function(df, row_indices, column_starts, end)
{
  # TODO: R-ify? Good damn luck.
  # Problem stems from the only way to store a bunch of vectors (the date index range of each numerical trackers counting) is a list
  # But when you flatten this list via unlist it combines all the vectors into one big long useless list of a bunch of indices
  # Since no R functions seem to be working (caught up on numerics, lists, no vectors of vectors, etc.)
  # I'M DOIN THIS MY DAMN SELF
  sum <- 0
  amount_of_dates_trackers_were_done[names(row_indices)] <<- 0
  
  # This case will happen when the dates quantification started for all tracker rows begin after the specified end date
  # Loop will still run from 1:0, so you have to explicitly return it
  if (length (column_starts) <= 0)
    return()
  
  for (i in 1:length(column_starts))
  {
    column_indices <- as.numeric(column_starts[i]:end)
    row <- dailE[as.numeric(unlist(row_indices[i], use.names = FALSE)), column_indices]
    
    # Initializes temporary vector to store numerical tracker row data
    temp_vector <- c()
    
    for (number in row)
    {
      
      # Adds to list representing each cell in row for numerical tracker
      # So basically temp_vector mimics the row you see in excel of numerical data
      temp_vector <- c(temp_vector, number)
      
      # Adds to numerical tracker sum
      if (number != '-' && !is.na(number) && number != 0)
      {
        sum <- sum + as.numeric(number)
        amount_of_dates_trackers_were_done[names(row_indices)[i]] <<- as.numeric(amount_of_dates_trackers_were_done[names(row_indices)[i]]) + 1
      }
    }
    totals_from_trackers[names(row_indices)[i]] <<- sum
    amount_of_dates_tracked[names(row_indices)[i]] <<- length(column_indices)
    sum <- 0
    
    # Needed double square brackets to work without replacement length error
    numerical_tracker_vectors[[names(row_indices)[i]]] <<- temp_vector
    
    # Gets mins & maxes
    # Removes hyphens and NAs from selection
    temp_vector <- temp_vector[!temp_vector %in% c("-") & !is.na(temp_vector)]
    
    max_of_trackers[[names(row_indices)[i]]] <<- max(as.numeric(temp_vector, na.rm = TRUE))
    min_of_trackers[[names(row_indices)[i]]] <<- min(as.numeric(temp_vector, na.rm = TRUE))
  }
}


# AVERAGES
calculate_averages <- function()
{
  averages_from_trackers[names(totals_from_trackers)] <<- unlist(totals_from_trackers, use.names = FALSE) / unlist(amount_of_dates_tracked, use.names = FALSE)
  
  average_amount_of_things_done_per_day()
  
  # The below has a dependency from calculate_totals -- totals_from_all_rows
  overall_average_each_row_done()
  
  average_amount_of_days_completed()
}

overall_average_each_row_done <- function()
{
  # Gets total times trackers were done
  tracker_indices <- which(!is.na(dailE_info$"Numerical Tracker?"))
  tracker_names <- dailE_info[tracker_indices, 1]
  tracker_indices <- which (names(totals_from_all_rows) %in% unlist(tracker_names))
  totals_of_times_trackers_done <<- totals_from_all_rows[tracker_indices]
  # Finds amount of days from tracker start date to end date
  amount_of_days_tracker_included <<- get_amount_of_days_between_thing_start_and_end_date(tracker_indices)
  
  # Gets total times things were done
  thing_indices <- which(is.na(dailE_info$"Shouldn't be counted in to-dos") & is.na(dailE_info$"Numerical Tracker?"))
  thing_names <- dailE_info[thing_indices, 1]
  thing_indices <- which (names(totals_from_all_rows) %in% unlist(thing_names))
  totals_of_times_things_done <<- totals_from_all_rows[thing_indices]
  # Finds amount of days from thing start date to end date
  amount_of_days_things_included <<- get_amount_of_days_between_thing_start_and_end_date(thing_indices)
  
  # Actual percentages of amount of days trackers and things done were actually done
  percentage_of_days_trackers_completed[names(totals_of_times_trackers_done)] <<- unlist(totals_of_times_trackers_done) / unlist(amount_of_days_tracker_included)
  percentage_of_days_trackers_completed <<- unlist(percentage_of_days_trackers_completed) * 100
  
  percentage_of_days_things_completed[names(totals_of_times_things_done)] <<- unlist(totals_of_times_things_done) / unlist(amount_of_days_things_included)
  percentage_of_days_things_completed <<- unlist(percentage_of_days_things_completed) * 100
}

average_amount_of_days_completed <- function()
{
  # Gets what non-real days are within input range
  blank_dates_within_range <<- blank_dates[which(blank_dates < end_date & blank_dates > start_date)]
  # Total amount of days list could've been done
  amount_of_potential_days <<- length(blank_dates_within_range) + amount_of_real_days
  percentage_of_days_not_done <- length(blank_dates_within_range) / amount_of_potential_days
  percentage_of_days_not_done <- percentage_of_days_not_done * 100
  percentage_of_days_completed <<- 100 - percentage_of_days_not_done
}

average_amount_of_things_done_per_day <- function()
{
  average_things_done_in_range_percentage[names(total_of_things_done_at_date)] <<- 0
  average_things_done_in_range_percentage[] <<- unlist(total_of_things_done_at_date, use.names = FALSE) / amount_of_days_in_range

  average_things_done_in_range_percentage[] <<- unlist(average_things_done_in_range_percentage, use.names = FALSE) / unlist(amount_of_things_to_do_at_date, use.names = FALSE)
  average_things_done_in_range_percentage[] <<- unlist(average_things_done_in_range_percentage, use.names = FALSE) * 100
  
  average_things_done_in_range_daily_number[names(average_things_done_in_range_percentage)] <<- 0
  average_things_done_in_range_daily_number[] <<- unlist(amount_of_things_to_do_at_date, use.names = FALSE) * (unlist(average_things_done_in_range_percentage, use.names = FALSE) / 100)
  
  average_overall_things_done_per_day_percentage <<- mean(unlist(average_things_done_in_range_percentage, use.names = FALSE))
  average_overall_things_done_per_day_number <<- mean(unlist(average_things_done_in_range_daily_number, use.names = FALSE))
  
  average_amount_of_things_to_do <<- mean(unlist(amount_of_things_to_do_at_date, use.names = FALSE))
}




###########################################    PRINTING FUNCTIONS    ###########################################
print_totals <- function(display_days = FALSE, show_how_many_times_completed_things = FALSE, show_word_totals = F)
{
  cat ("\n\n##################    DATA TOTALS    ##################\n")
  cat ("\nThere are", sum_of_all_rows, "rows")
  cat ("\nThere are", sum_of_things_to_do, "things to do")
  cat ("\nThere are", sum_of_trackers, "trackers\n")
  cat ("\nThere are", amount_of_real_days, "days completed")
  # TODO: Put improving yourself since <starting date>
  cat ("\n", sum_of_all_things_done, "steps done towards improving yourself! :)\n")
  
  if (display_days)
  {
    if (show_how_many_times_completed_things)
    {
      cat ("\n\n##################   TOTAL THINGS COMPLETED    ##################\n")
      for (i in 1:length(totals_of_times_things_done))
        cat ("\n", names(totals_of_times_things_done)[i], "done", unlist(totals_of_times_things_done)[i], "times over", unlist(amount_of_days_things_included)[i], "days")
      
      cat ("\n\n##################   TOTAL TRACKERS COMPLETED    ##################\n")
      for (i in 1:length(totals_of_times_trackers_done))
        cat ("\n", names(totals_of_times_trackers_done)[i], "done", unlist(totals_of_times_trackers_done)[i], "times over", unlist(amount_of_days_tracker_included)[i], "days")
    }
  }
  else
  {
    if (show_how_many_times_completed_things)
    {
      cat ("\n\n##################   TOTAL THINGS COMPLETED    ##################\n")
      for (i in 1:length(totals_of_times_things_done))
        cat ("\n", names(totals_of_times_things_done)[i], "done", unlist(totals_of_times_things_done)[i], "times")
      
      cat ("\n\n##################   TOTAL TRACKERS COMPLETED    ##################\n")
      for (i in 1:length(totals_of_times_trackers_done))
        cat ("\n", names(totals_of_times_trackers_done)[i], "done", unlist(totals_of_times_trackers_done)[i], "times")
    }
  }
  
  # TODO: Make this specific for each row!
  if (length(totals_from_trackers) > 0)
  {
    if (display_days)
    {
      cat ("\n\n##################    TRACKER TOTALS    ##################\n")
      for (i in 1:length(totals_from_trackers))
        cat ("\n", names(totals_from_trackers)[i], ":", unlist(totals_from_trackers[i], use.names = FALSE), "over", unlist(amount_of_dates_tracked[i], use.names = FALSE), "days")
    }
    else
    {
      cat ("\n\n##################    TRACKER TOTALS    ##################\n")
      for (i in 1:length(totals_from_trackers))
        cat ("\n", names(totals_from_trackers)[i], ":", unlist(totals_from_trackers[i], use.names = FALSE))
    }
  }
  
  if (show_word_totals)
  {
    cat ("\n\n##################    MISC TOTALS    ##################\n")
    #TODO: change amount of days words counted for based off of first typed row content meaningful entry (not just x)
    # If end date is before this date, print message saying end date is before you actually started typing meaningful stuff
    if (display_days)
    {
      for (i in 1:length(amount_of_times_words_mentioned))
        cat ("\n", names(amount_of_times_words_mentioned)[i], "mentioned", unlist(amount_of_times_words_mentioned)[i], "times over", amount_of_real_days, "days")
    }
    else
    {
      for (i in 1:length(amount_of_times_words_mentioned))
        cat ("\n", names(amount_of_times_words_mentioned)[i], "mentioned", unlist(amount_of_times_words_mentioned)[i], "times") 
    }
    cat("\n")
  }
}

print_max_min <- function(max = TRUE, min = TRUE)
{
  # TODO: Include units in output
  if (max)
  {
    cat ("\n\n##################   TRACKER MAXIMUMS    ##################\n")
    for (i in 1:length(max_of_trackers))
      cat ("\n", names(max_of_trackers)[i], ":", unlist(max_of_trackers)[i]) 
  }
  if (min)
  {
    cat ("\n\n##################   TRACKER MINIMUMS    ##################\n")
    for (i in 1:length(min_of_trackers))
      cat ("\n", names(min_of_trackers)[i], ":", unlist(min_of_trackers)[i]) 
  }
}

print_averages <- function(display_days = FALSE, display_percentage_of_real_days_done = FALSE, include_days_not_done = TRUE)
{
  # If including only days the trackers were done, overwrite the averages vector
  if (!include_days_not_done)
    averages_from_trackers[names(totals_from_trackers)] <<- unlist(totals_from_trackers, use.names = FALSE) / unlist(amount_of_dates_trackers_were_done, use.names = FALSE)
  
  if (display_days)
  {
    # Shows percentage of day tracker was done out of all real days
    if (display_percentage_of_real_days_done)
    {
      # TODO: sort by order in dailE excel (only way to access prolly thru OG_dailE)
      cat ("\n\n##################   AVERAGE THING COMPLETION    ##################\n")
      for (i in 1:length(percentage_of_days_things_completed))
        cat ("\n", names(percentage_of_days_things_completed)[i], "done", print_decimal_places(percentage_of_days_things_completed[i], 0), "% of", unlist(amount_of_days_things_included)[i],"days")
      
      cat ("\n\n##################   AVERAGE TRACKER COMPLETION    ##################\n")
      for (i in 1:length(percentage_of_days_trackers_completed))
        cat ("\n", names(percentage_of_days_trackers_completed)[i], "done", print_decimal_places(percentage_of_days_trackers_completed[i], 0), "% of", unlist(amount_of_days_tracker_included)[i],"days")
    }
    
    # TRACKER AVERAGES
    if (length(averages_from_trackers) > 0)
    {
      cat ("\n\n##################   TRACKER AVERAGES    ##################\n")
      
      if (!include_days_not_done)
      {
        for (i in 1:length(averages_from_trackers))
          cat ("\n", names(averages_from_trackers)[i], "average of", print_decimal_places(unlist(averages_from_trackers[i], use.names = FALSE), 1), "per day over", unlist(amount_of_dates_trackers_were_done[i], use.names = FALSE), "days")
      }
      else
      {
        for (i in 1:length(averages_from_trackers))
          cat ("\n", names(averages_from_trackers)[i], "average of", print_decimal_places(unlist(averages_from_trackers[i], use.names = FALSE), 1), "per day over", unlist(amount_of_dates_tracked[i], use.names = FALSE), "days")
      }
    }
    
    cat ("\n\n##################    GENERAL AVERAGES   ##################\n")
    cat ("\n", print_decimal_places(percentage_of_days_completed, 0), "% (",  amount_of_real_days, "days) of", amount_of_potential_days, "potential days completed -- so", length(blank_dates_within_range), "days not done")
    
    # THINGS DONE AVERAGES
    #print_date_range_averages()
    cat ("\nOverall average of things done per day:", print_decimal_places(average_overall_things_done_per_day_percentage, 0), "%, or about", print_decimal_places(average_overall_things_done_per_day_number, 0), "things (over", amount_of_real_days, "days)")
    
    # SOBER AVERAGE
    # Subtract from total days to find days sober
    # Not sober in list so can visualize days spent not sober
    sober_average <- amount_of_real_days - as.numeric(totals_from_all_rows["Not Sober"])
    sober_average <- (sober_average / amount_of_real_days) * 100
    cat ("\nSober", print_decimal_places((sober_average), 0), "% of", amount_of_real_days, "of recorded days\n")
  }
  else
  {
    # Shows percentage of day tracker was done out of all real days
    if (display_percentage_of_real_days_done)
    {
      # TODO: sort by order in dailE excel (only way to access prolly thru OG_dailE)
      cat ("\n\n##################   AVERAGE THING COMPLETION    ##################\n")
      for (i in 1:length(percentage_of_days_things_completed))
        cat ("\n", names(percentage_of_days_things_completed)[i], "done", print_decimal_places(percentage_of_days_things_completed[i], 0), "% of days")
      
      cat ("\n\n##################   AVERAGE TRACKER COMPLETION    ##################\n")
      for (i in 1:length(percentage_of_days_trackers_completed))
        cat ("\n", names(percentage_of_days_trackers_completed)[i], "done", print_decimal_places(percentage_of_days_trackers_completed[i], 0), "% of days")
    }
    
    # TRACKER AVERAGES
    if (length(averages_from_trackers))
    {
      cat ("\n\n##################   TRACKER AVERAGES    ##################\n")
      
      if (!include_days_not_done)
      {
        for (i in 1:length(averages_from_trackers))
          cat ("\n", names(averages_from_trackers)[i], "average of", print_decimal_places(unlist(averages_from_trackers[i], use.names = FALSE), 1), "per day")
      }
      else
      {
        for (i in 1:length(averages_from_trackers))
          cat ("\n", names(averages_from_trackers)[i], "average of", print_decimal_places(unlist(averages_from_trackers[i], use.names = FALSE), 1), "per day")
      }
    }
    
    cat ("\n\n##################    GENERAL AVERAGES   ##################\n")
    cat ("\n", print_decimal_places(percentage_of_days_completed, 0), "% of days completed")
    
    # THINGS DONE AVERAGES
    #print_date_range_averages()
    cat ("\nOverall average of things done per day:", print_decimal_places(average_overall_things_done_per_day_percentage, 0), "%, or about", print_decimal_places(average_overall_things_done_per_day_number, 0), "things")
    
    # SOBER AVERAGE
    # Subtract from total days to find dys sober
    # Not sober in list so can visualize days spent not sober
    sober_average <- amount_of_real_days - as.numeric(totals_from_all_rows["Not Sober"])
    sober_average <- (sober_average / amount_of_real_days) * 100
    cat ("\nSober", print_decimal_places((sober_average), 0), "%\n")  
  }
}

print_date_range_averages <- function()
{
  for (i in 1:length(average_things_done_in_range_percentage))
  {
    # TODO: Change this so end date is a local variable
    # So in if statement can just change value of that and only have to edit one text field to update
    if (i == length(average_things_done_in_range_percentage))
      cat ("\nFrom", names(average_things_done_in_range_percentage)[i], "to", printable_date_from_int(end_date), "average of", print_decimal_places(unlist(average_things_done_in_range_percentage[i], use.names = FALSE), 0), "% (", print_decimal_places(unlist(average_things_done_in_range_daily_number[i], use.names = FALSE), 0), "things) done per day")
    else
      cat ("\nFrom", names(average_things_done_in_range_percentage)[i], "to", names(average_things_done_in_range_percentage)[i+1], "average of", print_decimal_places(unlist(average_things_done_in_range_percentage[i], use.names = FALSE), 0), "% (", print_decimal_places(unlist(average_things_done_in_range_daily_number[i], use.names = FALSE), 0), "things) done per day")
  }
}

print_quantification_start <- function()
{
  # TODO: Vectorize string with each element lol
  cat(names(date_when_tracker_quantification_started), "started tracking time on", printable_date_from_int(unlist(date_when_tracker_quantification_started)))
}

print_decimal_places <- function(num, n = 2)
{
  return (format(round(num, n), nsmall = n))
}



###### Main Function -----------------------------------------------------------
main <- function()
{
  # main function that calls entire script
  initializers()
  calculators()
  
  #graph()
  #print_totals(display_days = F, show_how_many_times_completed_things = TRUE, show_word_totals = T)
  #print_max_min()
  #print_averages(display_days = T, display_percentage_of_real_days_done = TRUE, include_days_not_done = T)
  
  #print (unlist(dailE[, 1]))
}

main()