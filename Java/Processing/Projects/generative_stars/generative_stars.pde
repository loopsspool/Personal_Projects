int STAR_SIZE = 50;  // Recommend keeping this size
int STAR_SIDES = 8;

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
    // Larger parameter moves curves closer to outside, smaller to inside
      // 0 is pretty cool too
      // Same with negative numbers
    star(-8);
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
  float sx;
  float sy;
  beginShape();
    // 2 * TWO_PI to give it that kind of sketched look
      // + (2 * angle) to give the final curve a natural finish (by adding another that draws over)
    for (float a = angle; a < TWO_PI + (2 * angle); a += angle)
    {
      loop_acc++;
      
      // Setting inner points
      // If it's the first point, this conditional sets it so its not at a corner
        // or middle of an arc so the curve doesn't sharpen at a point
      if (a == angle)
      {
        sx = cos(a - half_angle/1.1) * curve_point;
        sy = sin(a - half_angle/1.1) * curve_point;
      }
      else
      {
        // To change angle of star, change what's after a-(half_angle/2)
        sx = cos(a-half_angle) * curve_point;
        sy = sin(a-half_angle) * curve_point;
      }
      curveVertex(sx, sy);
      // If first point, set first curve anchor point (necessary by curveVertex)
      if (a == angle)
        curveVertex(sx, sy);
        
      // Outtermost points
      sx = cos(a) * STAR_SIZE;
      sy = sin(a) * STAR_SIZE;
      
      // Smoothing the final curve
      if (loop_acc >= (STAR_SIDES + 1))
      {
        sx = cos(a) * STAR_SIZE;
        sy = sin(a) * STAR_SIZE;
        curveVertex(sx, sy);

        // DO NOT TAKE THIS OUT
        // Otherwise the loop will continue and draw a wrong line
        break;
      }
      else
        curveVertex(sx, sy);
    }
  endShape(CLOSE);
}
