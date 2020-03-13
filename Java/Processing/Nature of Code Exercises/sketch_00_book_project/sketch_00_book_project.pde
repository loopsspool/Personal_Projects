rocket[] rockets;

void setup()
{
  size(2400, 1200);
  colorMode(HSB, 360, 100, 100);
  
  rockets = new rocket[5];
  for (int i = 0; i < 5; i++)
  {
    rockets[i] = new rocket();
  }
}

void draw()
{
  push();
  noStroke();
  fill(214, 80, 8, 70);
  rect(0, 0, width, height);
  pop();
  
  for (int i = 0; i < 5; i++)
  {
    rockets[i].update();
    rockets[i].display();
  }
}
