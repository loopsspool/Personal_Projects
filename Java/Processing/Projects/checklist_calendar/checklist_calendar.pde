import java.util.*;  // For Date
import java.time.*;  // For LocalDate
import processing.pdf.*;  // To convert to PDF
import geomerative.*;  // For text outline

// PDF Switcher
boolean is_PDF = false;

// GENERAL DATE STUFF
String[] WEEKDAYS = {"MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"};

// CURENT DATE STUFF
Date CURRENT_DATE;
LocalDate LOCAL_DATE;
int YEAR, MONTH, DAY;
String DAY_NAME;
String MONTH_NAME;
String MONTH_AND_YEAR;
String FIRST_DAY_OF_MONTH_NAME;
int FIRST_DAY_OF_MONTH_COLUMN;
int DAYS_IN_MONTH;

// CALENDAR ALIGNMENTS
int MONTH_TEXT_SIZE = 60;
float MONTH_BOX_HEIGHT;
float DAY_NAME_BOX_HEIGHT = 25;

// CALENDAR GRID INFO
int AMOUNT_OF_ROWS;
int outline_buffer = 3;  // For visibility & so outline matches line weight below month & weekday names

// FONTS
RFont default_month_font;
PFont month_font;
PFont body_text;
PFont body_text_bold;

// GRAPHICS
PGraphics month_banner;


// TODO: Make it so outline_buffer from outline is factored into gridlines/day numbers/checkbox margin
void settings()
{
  // When adjusting sketch size for ease of printing, change checklist y-adjustments and text size
  if (is_PDF)
  {
    size(748, 575, PDF, "calendar_test.pdf");
  }
  else
  {
    size(748, 575);
    noLoop();
  }
}

void setup()
{
  surface.setLocation(50, 50);
  colorMode(HSB, 360, 100, 100, 100);
  textAlign(CENTER, CENTER);
  strokeCap(SQUARE);
  background(360);
  
  // Uncomment to view available fonts
  //String[] fontList = PFont.list();
  //printArray(fontList);
  RG.init(this);  // Initializes geomerative stuff
  default_month_font = new RFont("data\\CASTELAR.TTF", 60, RFont.CENTER);
  month_font = createFont("Castellar", 60);
  body_text = createFont("Century Schoolbook", 12);
  body_text_bold = createFont("Century Schoolbook Bold", 12);
  
  // CALENDAR ALIGNMENT
  MONTH_BOX_HEIGHT = height/6;
  
  // DATE STUFF
  CURRENT_DATE = new Date();
  LOCAL_DATE = CURRENT_DATE.toInstant().atZone(ZoneId.systemDefault()).toLocalDate();
  //LOCAL_DATE = LOCAL_DATE.plusMonths(1);
  YEAR = LOCAL_DATE.getYear();
  MONTH = LOCAL_DATE.getMonthValue();
  DAY = LOCAL_DATE.getDayOfMonth();
  MONTH_NAME = LOCAL_DATE.getMonth().toString();
  FIRST_DAY_OF_MONTH_NAME = LOCAL_DATE.minusDays(DAY-1).getDayOfWeek().toString();
  MONTH_AND_YEAR = MONTH_NAME + " " + YEAR;
  DAYS_IN_MONTH = LOCAL_DATE.lengthOfMonth();
  
  // GRID STUFF
  AMOUNT_OF_ROWS = 5;
  
  // Finding what column month starts in
  FIRST_DAY_OF_MONTH_COLUMN = 0;
  while (WEEKDAYS[FIRST_DAY_OF_MONTH_COLUMN] != FIRST_DAY_OF_MONTH_NAME)
    FIRST_DAY_OF_MONTH_COLUMN++;
  
  // Adding a row if days don't fit into 7x5 grid
    // If longer month starts later in the week
  int DAYS_FITTING_INTO_7X5 = 35 - FIRST_DAY_OF_MONTH_COLUMN;
  if (DAYS_FITTING_INTO_7X5 < DAYS_IN_MONTH)
    AMOUNT_OF_ROWS = 6;
  
  // If February starts on a Monday and it isn't a leap year it only needs 4 rows
  if ((DAYS_IN_MONTH == 28) && (FIRST_DAY_OF_MONTH_COLUMN == 0))
    AMOUNT_OF_ROWS = 4;

}

void draw()
{
  
  month_art();
  month_art_cutoff();
  grid_lines();
  weekday_names();
  iterate_through_month("Numbers");
  iterate_through_month("Checklist");
  iterate_through_month("Grey Boxes");
  calendar_outline();
    
  if (is_PDF)
    exit();
}

void month_art_cutoff()
{
  // White box covering any overlap from the monthly art header
  push();
    noStroke();
    fill(360);
    rect(0, MONTH_BOX_HEIGHT, width, height);
  pop();
}

void grid_lines()
{
  push();
    strokeWeight(1);
    stroke(0);
    translate(0, MONTH_BOX_HEIGHT);
    // VERTICAL LINES
    float x;
    for (int i = 1; i < 7; i++)
    {
      // + outline_buffer to make all squares display the same
        // left row was being cut into by outline
      x = (i * (width/7)) + outline_buffer;
      line(x, 0, x, height);
    }
    
    // HORIZONTAL LINES
    translate(0, DAY_NAME_BOX_HEIGHT);
    
    float y;
    for (int i = 1; i < AMOUNT_OF_ROWS; i++)
    {
      // - outline_buffer to make all squares display the same
        // bottom row was being cut into by outline
      y = i * ((height - outline_buffer - (MONTH_BOX_HEIGHT + DAY_NAME_BOX_HEIGHT))/AMOUNT_OF_ROWS);
      line(0, y, width, y);
    }
  pop();
}

void weekday_names()
{
  textFont(body_text_bold);
  
  push();
    // Border lines
    stroke(0);
    strokeWeight(2);
    line(0, MONTH_BOX_HEIGHT, width, MONTH_BOX_HEIGHT);
    line(0, MONTH_BOX_HEIGHT + DAY_NAME_BOX_HEIGHT, width, MONTH_BOX_HEIGHT + DAY_NAME_BOX_HEIGHT);
    
    // Actual day names 
    translate(0, MONTH_BOX_HEIGHT + DAY_NAME_BOX_HEIGHT);
    noStroke();
    fill(0);
    textFont(body_text_bold);
    textSize(14);
    for (int i = 0; i < 7; i++)
      // + width/14 to center text between lines
      // + outline_buffer to adjust for column adjustment from outline
      text(WEEKDAYS[i], (i * width/7) + width/14 + outline_buffer, -(DAY_NAME_BOX_HEIGHT/2) - 2); 
  pop();
}

void iterate_through_month(String doing)
{
  int square_acc = 0;
  int day_acc = 0;
  
  // If month starts on a Monday (first square), make it day 1
      // So square doesn't get greyed out & day number shows as 1
        // Since normally isn't accumulated until after function calls
  if (FIRST_DAY_OF_MONTH_COLUMN == 0)
    day_acc++;
      
  push();  
    translate(outline_buffer, MONTH_BOX_HEIGHT + DAY_NAME_BOX_HEIGHT);
    float x_translate_added = 0;  // This is to accurately realignwhen the y-axis moves down
    
    for (int y_ = 0; y_ < AMOUNT_OF_ROWS; y_++)
    {
      for (int x_ = 0; x_ < 7; x_++)
      {
        switch(doing)
        {
          case "Grey Boxes":
            grey_out_non_month_days(day_acc);
            break;
            
          case "Numbers":
            number_display(day_acc);
            break;
            
          case "Checklist":
            daily_text();
            break;
        }
        
        // Moving onto next day
        square_acc++;
        if (square_acc >= FIRST_DAY_OF_MONTH_COLUMN)
          day_acc++;
          
        translate(width/7, 0);
        x_translate_added += width/7;
      }
      // Moving onto next week
      translate(-x_translate_added, ((height - outline_buffer - (MONTH_BOX_HEIGHT + DAY_NAME_BOX_HEIGHT))/AMOUNT_OF_ROWS));
      x_translate_added = 0;  // Resetting x to beginning of week
    }
  pop();
}

void number_display(int day_num)
{ 
  int x_buffer = 4;
  int y_buffer = 8;
  
  push();
    translate(x_buffer, y_buffer);
    textAlign(LEFT, CENTER);
    textFont(body_text_bold);
    textSize(12);
    stroke(0);
    fill(0);
    text(String.valueOf(day_num), 0, 0);
  pop();
}

void grey_out_non_month_days(int day)
{
  push();
    stroke(0);
    fill(280);
    if (day < 1)
    {
      // TODO: First box not aligned to edge
      // Greying out days before month start
      rect(0, 0, width/7, ((height - outline_buffer - (MONTH_BOX_HEIGHT + DAY_NAME_BOX_HEIGHT))/AMOUNT_OF_ROWS));
    }
    if (day > DAYS_IN_MONTH)
    {
      // Greying out days after month ends
        // + 5 on height/width because last row/column might be slightly larger? Due to width/7 whatevers left after saturday line
      rect(0, 0, + width/7 + 5, ((height - (MONTH_BOX_HEIGHT + DAY_NAME_BOX_HEIGHT))/AMOUNT_OF_ROWS) + 5);
    }
  pop();
}

void daily_text()
{
  textFont(body_text);
  
  push();
    translate(4, 5.5);
    bullet_point("Do morning routine");
    bullet_point("Be present");
    bullet_point("Do thing you love");
    bullet_point("Spend time w/ self");
    bullet_point("Do list");
  pop();
}

void bullet_point(String text)
{
  float indent = 13;
  float size = 9.4;
  float y_translate = 0;
  // Adjusting for rows of calendar so alignment doesn't look funky
  // TODO: Align to liking
  if (AMOUNT_OF_ROWS == 6)
    y_translate = 11.7;
  if (AMOUNT_OF_ROWS == 5)
    y_translate = 14.5;
  if (AMOUNT_OF_ROWS == 4)
    y_translate = 18;

  // No push/pop so translates will stack for bullet points
  translate(0, y_translate);
  square(0, 0, size);
  textSize(size);
  textAlign(LEFT);
  fill(0);
  text(text, indent, 0.9 * size);
  noFill();  // Keep this here so following check-boxes aren't filled
}

void calendar_outline()
{
  // TODO: Left outline line not locked to window edge?
  push();
    stroke(0);
    strokeWeight(outline_buffer + 1);
    line(0, 0, 0, height);  // LEFT
    line(width, 0, width, height);  // RIGHT
    line(0, 0, width, 0);  // TOP
    line(0, height, width, height);  // BOTTOM
  pop();
}

void draw_text(font_class Font)
{
  push();
    if (Font.is_bolded)
      bold_font(Font);
    else
    {
      Font.set_features();
      Font.display();
    }
  pop();
}

void bold_font(font_class Font)
{
  push();
    Font.set_features();
    // "Bolds" the font a little -- since theres no bold versions of some fonts
    float x_shift_divisor = 5;  // To utilize i as coordinate, small shifts in x
    for (float i = 0; i < Font.bold_weight/x_shift_divisor; i += 1/x_shift_divisor)
    {
      translate(i, 0);
      Font.display();
    }
  pop();
}

/** 
TODO: Text effects: 
  - 3D gradually increasing font size
  - Text Fade in/out
  + See what geomerative can do
**/ 
