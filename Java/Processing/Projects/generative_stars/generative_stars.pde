int STAR_SIZE = 50;
int STAR_SIDES = 14;

void setup()
{
  size(800, 800);
  surface.setLocation(50, 50);
  colorMode(HSB, 360, 100, 100, 100);
  
  strokeWeight(2);
  //curveTightness(-1);
}

void draw()
{
  push();
    translate(width/2, height/2);
    star(20);
  pop();
}

// Courtesy of https://processing.org/examples/star.html
  // Modified a bit to make curved stars
void star(float curve_point) 
{
  noFill();
  int loop_acc = 0;
  float angle = radians(360 / float(STAR_SIDES));
  float half_angle = angle/2.0;
  beginShape();
  // 2 * TWO_PI to give it that kind of sketched look
    // + angle to give the final curve a natural finish
  for (float a = angle; a <= (2 * TWO_PI) + (2 * angle); a += angle)
  {
    loop_acc++;
    // Outtermost points
    float sx = cos(a) * STAR_SIZE;
    float sy = sin(a) * STAR_SIZE;
    curveVertex(sx, sy);
    // If first point, set first curve anchor point (necessary by curveVertex)
    if (a == angle)
      curveVertex(sx, sy);
    // Setting inner points
    sx = cos(a+half_angle) * curve_point;
    sy = sin(a+half_angle) * curve_point;
    curveVertex(sx, sy);
    // Smoothing the final curve
    // This is where the error occurs on stars with less points
    if (loop_acc >= (2 * STAR_SIDES) + 1)
    {
      // Directing the last curve is where you're gonna fix the straight line
        // On the final curve
      //sx = cos(0) * STAR_SIZE;
      //sy = sin(0) * STAR_SIZE;
      //curveVertex(sx, sy);
      sx = cos(angle) * STAR_SIZE;
      sy = sin(angle) * STAR_SIZE;
      //sx = cos(a+half_angle) * curve_point;
      //sy = sin(a+half_angle) * curve_point;
      curveVertex(sx, sy);
    }
  }
  endShape(CLOSE);
}
