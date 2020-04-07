// Used to evaluate time between born date and today
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

// TODO: Add months!
HashMap<String, Integer> EXPECTED;  // Life expectancy in years, weeks, and days
int EXPECTED_YEARS;  // Expectancy to base years, weeks, and days expectancy
int LIVED;  // How long you've lived in days
HashMap<String, Integer> LIVED_YEARS;  // Maps days lived to weeks and years
int REMAINING;
String SELECTED_INTERVAL;  // How grid shows up (days, weeks, years)

int SCALE;  // Size of squares based off window width & height
int COLS, ROWS;
int SQUARE_ACC;  // Tracks square count

void setup()
{
  size(800, 800);
  // Makes it so when sketch pops up doesn't interfere with code window
  surface.setLocation(70, 100);
  colorMode(HSB, 360, 100, 100);
  
  LIVED = int(days_between("1998-10-24"));
  println(LIVED);
  // TODO: Generate HashMap based off of lived days
  
  EXPECTED_YEARS = 80;
  SELECTED_INTERVAL = "DAYS";
  
  EXPECTED = new HashMap<String, Integer>();
  EXPECTED.put("YEARS", EXPECTED_YEARS);
  EXPECTED.put("WEEKS", EXPECTED_YEARS * 52);
  EXPECTED.put("DAYS", EXPECTED_YEARS * 365);
  
  SQUARE_ACC = 0;
  // Finds next perfect square for grid size
    // Consequence of this is the grid will always attempt to be as square as possible
      // So sometimes doesn't fill screen nicely (ie expectancy interval of days)
  int grid_size = floor(sqrt(EXPECTED.get(SELECTED_INTERVAL))) + 1;
  COLS = grid_size;
  ROWS = grid_size;
  SCALE = width / COLS;

  background(0);
  // TODO: Change colors of squares based off lived or not
  fill(360);
  stroke(0);
  
  // Label used to break outer loop from inner loop
  outer_loop:
  for (int y = 0; y < ROWS; y++)
  {
    for (int x = 0; x < COLS; x++)
    {
      // Tracks squares made so grid doesn't exceed expectancy
      SQUARE_ACC++;
      if (SQUARE_ACC > EXPECTED.get(SELECTED_INTERVAL))
        break outer_loop;
      square(x * SCALE, y * SCALE, SCALE);
    }
  }
  
}

void draw()
{

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
