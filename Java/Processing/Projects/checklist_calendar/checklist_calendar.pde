import java.util.*;
import processing.pdf.*;

Date current_date;

void setup()
{
  size(2550, 3300, PDF, "calendar_test.pdf");
  colorMode(HSB, 360, 100, 100, 100);
  
  current_date = new Date();
  
}

void draw()
{
  exit();
}
