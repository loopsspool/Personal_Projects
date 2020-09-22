void setup()
{
  size(800, 800);
  surface.setLocation(50, 50);
  
  colorMode(HSB, 360, 100, 100, 100);
  background(0);
  noLoop();
}

void draw()
{
  push();
    stroke(360);
    noFill();
    strokeWeight(3);
    translate(width/2, height/2);
    int circle_d = 50;
    circle(0, 0, circle_d);
    
    int main_strings = 8;
    float rotation = 0;
    float[] rotation_array;
    rotation_array = new float [main_strings];
    // Main strings
    push();
      for (int i = 0; i < main_strings; i++)
      {
        rotation = radians(360/(main_strings + random(-4, 4)));
        rotation_array[i] = rotation;
        rotate(rotation);
        line(0, -circle_d/2, 0, -height);
      }
    pop();
    // Curves in between main strings
    for (int i = 0; i < main_strings; i++)
    {
      if (i == main_strings - 1)
      {
        // draw arc from [i] to [0]
        break;
      }
      else
      {
        // Puts axis at current main line
        rotate(rotation_array[i]);
        push();
          // Puts axis halfway between current main line and next
            // Negated by pop(), so will hop back to current main line so rotte will be accurate still
          rotate(rotation_array[i+1]/2);
          translate(0, -circle_d/2);
          stroke(#EA2FEA);
          line(0, 0, 0, -height);
          float x = 0;
          float y = 200;
          float inside_angle = rotation_array[i+1]/2;
          // TODO: Lines aren't quite reaching to main lines
            // Is this too complicated? Maybe just do even geometry?
          
          // Maybe instead of rotating to the half of each line, draw the arcs with
            // No rotate calls, just using sin and cosine
          translate(0, -y);
          x = (y * sin(inside_angle))/sin(radians(90) - inside_angle);
          line(-x, 0, x, 0);
        pop();
      }
    }
  pop();
}
