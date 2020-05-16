int STAR_SIZE = 300;
int STAR_SIDES = 4;

void setup()
{
  size(800, 800);
  surface.setLocation(50, 50);
  colorMode(HSB, 360, 100, 100, 100);
  
}

void draw()
{
  test_lines();
}

void test_lines()
{
  push();
    noFill();
    strokeWeight(3);
    
    translate(width/2, height/2);
    float angle = radians(360 / STAR_SIDES);
    for (int i = 0; i < STAR_SIDES; i++)
    {
      beginShape();
        curveVertex(0, -STAR_SIZE/2);
        curveVertex(0, -STAR_SIZE/2);
        curveVertex(STAR_SIZE/10, -STAR_SIZE/10);
        curveVertex(STAR_SIZE/2, 0);
        curveVertex(STAR_SIZE/2, 0);
      endShape();
      rotate(angle);
    }
  pop();
}
