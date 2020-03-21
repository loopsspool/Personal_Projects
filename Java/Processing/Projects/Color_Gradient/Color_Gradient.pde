color from;  // Starting color
color to;  // Ending color
int stroke_weight;
int amount_of_lines;  // Increase this to get a more fluid gradient
int gap;  // Gaps between the lines, measured in pixels

void setup()
{
    size(800, 800);
    // If in HSB just shifts color wheel through other colors
      // So use default RGB colorspace
    //colorMode(HSB, 360, 100, 100);
    
    //HSB colors
    //from = color(58, 100, 100);
    //to = color(313, 100, 100);
    
    // TODO: Create some sort of list of these that can be refrenced by name?
    // RGB colors
    //from = color(255, 247, 0);  // Yellow
    from = color(29, 255, 255);  // Neon blue
    //to = color(255, 0, 200);  // Hot pink
    to = color(0, 255, 213);
    
    amount_of_lines = 10;  // Increase this to get a more fluid gradient
    // Careful of gaps when line count is high
      // Big gaps should not be used on high line counts
    gap = 2;  // Gaps between the lines, measure in pixels
    // abs() for protection of gap value being higher than division
    stroke_weight = abs((height/amount_of_lines) - gap);  // So no line overlap (not visible anyways but eh)
    // Above 400 lines the lines on screen get so small unpredictable stuff happens
    if (amount_of_lines > 400)
      stroke_weight = 400;
    strokeWeight(stroke_weight);
    
    // Color of gaps, if any
    // IN RGB
    background(0);
}

void draw()
{ 
  for (int i = 1; i <= amount_of_lines; i++)
  {
    // Setting each line color to the gradient color
      // Float conversion so int division doesn't default it to 0 or 1
    stroke(lerpColor(from, to, float(i)/amount_of_lines));
    // Setting y coordinates for lines
      // i - 1 to start lines at the top of the screen
      // height/amount_of_lines to place each line at equal intervals
      // adding stroke_weight/2 so lines end at the bottom of the screen
    float y = ((i - 1) * height/amount_of_lines) + stroke_weight/2;
    // Actually drawing the line
    line(0, y, width, y);
  }
}
