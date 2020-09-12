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
    for (int i = 0; i < main_strings; i++)
    {
      rotation = 360/(main_strings + random(-4, 4));
      rotate(radians(rotation));
      line(sin(radians(rotation)) * circle_d/2, cos(radians(rotation)) * circle_d/2, sin(radians(rotation)) * width, cos(radians(rotation)) * height); 
      println(rotation);
  }
  pop();
}
