import java.util.ArrayList;

int STAR_SIZE = 100;
int STAR_POINTS;
int HIGHEST_POINTS_NUM = 20;

void setup()
{
  size(800, 800);
  surface.setLocation(50, 50);
  colorMode(HSB, 360, 100, 100, 100);
  noLoop();
  
  strokeWeight(2);
  //curveTightness(-1);
}

void draw()
{
  
  push();
    translate(width/2, height/2);
    star();
  pop();
}

// Courtesy of https://processing.org/examples/star.html
  // Modified a bit to make curved stars
void star() 
{
  // Amount of star points
  STAR_POINTS = floor(random(3, HIGHEST_POINTS_NUM));
  // Where the curve occurs (Larger parameter moves curves closer to outside, smaller to inside)
  int curve_point = floor(random(-STAR_SIZE, STAR_SIZE));
  
  int loop_acc = 0;
  float angle = radians(360 / float(STAR_POINTS));
  float half_angle = angle/2.0;
  float sx;
  float sy;
  
  float inner_curve_angle = random(half_angle/4, 10 * half_angle);
  float outer_curve_angle = radians(random(TWO_PI));
  
  noFill();
  beginShape();
    // + (2 * angle) to give the final curve a natural finish (by adding another that draws over)
    for (float a = angle; a <= TWO_PI + (2 * angle); a += angle)
    {
      loop_acc++;
      
      // Setting inner points
      // If it's the first point, this conditional sets it so its not at a corner
        // or middle of an arc so the curve doesn't sharpen at a point
      if (a == angle)
      {
        sx = cos(a - (half_angle/1.1)) * curve_point;
        sy = sin(a - (half_angle/1.1)) * curve_point;
      }
      else
      {
        // To change angle of star where it meets the center, change what's after a- eg (a-(half_angle/16))
          // If bigger positive multiples, the fingers look more like leaves (a-(10 * half_angle))
        // Also potentially changing independantly
        sx = cos(a - inner_curve_angle) * curve_point;
        sy = sin(a - inner_curve_angle) * curve_point;
      }
      curveVertex(sx, sy);
        
      // Outtermost points
      // To change angle of outtermost star points, change what's after a eg (a-1)
      sx = cos(a - outer_curve_angle) * STAR_SIZE;
      sy = sin(a - outer_curve_angle) * STAR_SIZE;
      curveVertex(sx, sy);
      
      // Drawing the final curve
      if (loop_acc >= (STAR_POINTS + 1))
      {
        // TODO: Last curve still comes out pointy
        curveVertex(sx, sy);

        // DO NOT TAKE THIS OUT
        // Otherwise the loop will continue and draw a wrong line
        break;
      }
    }
  endShape(CLOSE);
}

ArrayList multiples(int points)
{
  ArrayList<Integer> divisible_by = new ArrayList<Integer>();
  
  // Finds all numbers that can divide points number
  for (int i = 2; i <= HIGHEST_POINTS_NUM; i++)
  {
    if (points % i == 0)
      divisible_by.add(i);
  }
  
  return divisible_by;
}
