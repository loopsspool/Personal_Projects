int STAR_SIZE = 200;
int STAR_SIDES = 8;

void setup()
{
  size(800, 800);
  surface.setLocation(50, 50);
  colorMode(HSB, 360, 100, 100, 100);
  
}

void draw()
{
  push();
    translate(width/2, height/2);
    star(80);
  pop();
}

// Courtesy of https://processing.org/examples/star.html
  // Modified a bit to make curved stars
void star(float curve_point) 
{
  noFill();
  float angle = radians(360 / STAR_SIDES);
  float half_angle = angle/2.0;
  beginShape();
  for (float a = 0; a < TWO_PI; a += angle)
  {
    float sx = cos(a) * STAR_SIZE;
    float sy = sin(a) * STAR_SIZE;
    curveVertex(sx, sy);
    if ( a == 0)
      curveVertex(sx, sy);
    sx = cos(a+half_angle) * curve_point;
    sy = sin(a+half_angle) * curve_point;
    curveVertex(sx, sy);
    if (a+angle >= TWO_PI)
    {
      // Directing the last curve is where you're gonna fix the straight line
        // On the final curve
      sx = cos(a+angle) * STAR_SIZE;
      sy = sin(a+angle) * STAR_SIZE;
      curveVertex(sx, sy);
    }
  }
  endShape(CLOSE);
}
