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
    
    int main_strings = 12;
    float rotation = 0;
    float[] rotation_array;
    rotation_array = new float [main_strings];
    // Main strings
    for (int i = 0; i < main_strings; i++)
    {
      rotation = radians(360/(main_strings + random(-4, 4)));
      rotation_array[i] = rotation;
      rotate(rotation);
      line(sin(rotation) * circle_d/2, cos(rotation) * circle_d/2, sin(rotation) * width, cos(rotation) * height); 
    }
    for (int i = 0; i < main_strings; i++)
    {
      if (i == main_strings - 1)
      {
        // draw arc from [i] to [0]
        break;
      }
      else
      {
        // Puts rotation in between two main lines so arc endpoints are linear
        rotate((rotation_array[i] + rotation_array[i + 1])/2);
        line(-abs(sin(rotation_array[i + 1]) * 100), -abs(cos(rotation_array[i + 1]) * 100), sin(rotation_array[i]) * 100, -abs(cos(rotation_array[i]) * 100));
      }
    }
    println(rotation_array);
    // Curves in between main strings
  pop();
}
