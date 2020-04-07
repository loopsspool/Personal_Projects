// Used to evaluate time between born date and today
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

int EXPECTED_YEARS;  // Expectancy to base years, weeks, and days expectancy
HashMap<String, Integer> EXPECTED;  // Life expectancy in years, weeks, and days
int LIVED_DAYS;  // How long you've lived in days
HashMap<String, Integer> LIVED;  // Maps days lived to weeks and years
int ADULT_DAYS;
HashMap<String, Integer> ADULT_LIVED;
// TODO: Add in red squares/hashmap for years prior to being a teenager

// TODO: Add in text of remaining <selected_interval>
int REMAINING;
String SELECTED_INTERVAL;  // How grid shows up (days, weeks, months, years)

int SCALE;  // Size of squares based off window width & height
int COLS, ROWS;
int CURRENT_SQUARE;  // Tracks square count

void setup()
{
  // TODO: Make it easier to change window size and have grids adapt (some split)
  size(800, 800);
  // Makes it so when sketch pops up doesn't interfere with code window
  surface.setLocation(70, 100);
  colorMode(HSB, 360, 100, 100);
  
  // TODO: Format the string so you can write dates how you're used to
  LIVED_DAYS = int(days_between("1998-10-24"));
  // TODO: Color in half squares (using rect) for weeks/months/years unfinished
  LIVED = new HashMap<String, Integer>();
  LIVED.put("DAYS", LIVED_DAYS);
  LIVED.put("WEEKS", LIVED_DAYS / 7);
  // TODO: Possibly correct months to proper accuracy in the future
  LIVED.put("MONTHS", LIVED_DAYS / 30);
  LIVED.put("YEARS", LIVED_DAYS / 365);
  
  
  EXPECTED_YEARS = 80;
  EXPECTED = new HashMap<String, Integer>();
  EXPECTED.put("YEARS", EXPECTED_YEARS);
  EXPECTED.put("MONTHS", EXPECTED_YEARS * 12);
  EXPECTED.put("WEEKS", EXPECTED_YEARS * 52);
  EXPECTED.put("DAYS", EXPECTED_YEARS * 365);
  
  // TODO: Make this a variable to be added to born date so don't have to have exact date
  ADULT_DAYS = int(days_between("2016-10-24"));
  ADULT_LIVED = new HashMap<String, Integer>();
  //////////////////////  CAREFUL!!!  //////////////////////
    // This IS NOT a count of adult times lived!!!!
    // This IS the square count above where adult times are
      // TODO: Consider changing in the future?
  ADULT_LIVED.put("DAYS", LIVED.get("DAYS") - ADULT_DAYS);
  ADULT_LIVED.put("WEEKS", LIVED.get("WEEKS") - (ADULT_DAYS / 7));
  ADULT_LIVED.put("MONTHS", LIVED.get("MONTHS") - (ADULT_DAYS / 30));
  ADULT_LIVED.put("YEARS", LIVED.get("YEARS") - (ADULT_DAYS / 365));
  
  SELECTED_INTERVAL = "DAYS";
  CURRENT_SQUARE = 0;
  // Finds next perfect square for grid size
    // Consequence of this is the grid will always attempt to be as square as possible
      // So sometimes doesn't fill screen nicely (ie selected interval of days)
  int grid_size = floor(sqrt(EXPECTED.get(SELECTED_INTERVAL))) + 1;
  COLS = grid_size;
  ROWS = grid_size;
  SCALE = width / COLS;

  background(0);
  stroke(0);
  //noStroke();
  
  // Label used to break outer loop from inner loop
  outer_loop:
  for (int y = 0; y < ROWS; y++)
  {
    for (int x = 0; x < COLS; x++)
    {
      // Tracks squares made so grid doesn't exceed expectancy
      CURRENT_SQUARE++;
      if (CURRENT_SQUARE > EXPECTED.get(SELECTED_INTERVAL))
        break outer_loop;
      
      // If square is a lived day, shade yellow
      if (CURRENT_SQUARE <= LIVED.get(SELECTED_INTERVAL))
      {
        fill(62, 100, 100);
        // If square is an ADULT lived day, shade green
        if (CURRENT_SQUARE >= ADULT_LIVED.get(SELECTED_INTERVAL))
          fill(110, 100, 100);
      }
      // If square not lived yet, shade very light grey
      else
        fill(350);
      
      square(x * SCALE, y * SCALE, SCALE);
    }
  }
}

long days_between(String born_string)
{
  // Parses born date string into a LocalDate object to be compared w current date
  LocalDate born = LocalDate.parse(born_string);
  // Gets current date
  LocalDate current_date = LocalDate.now();
  // Figures out time between born date and today
  return ChronoUnit.DAYS.between(born, current_date);
}
