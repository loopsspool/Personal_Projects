rocket[] rockets;
int amount_of_rockets = 6;
asteroid[] asteroids;
int amount_of_asteroids = 8;

void setup()
{
  size(2400, 1200);
  colorMode(HSB, 360, 100, 100);
  
  rockets = new rocket[amount_of_rockets];
  for (int i = 0; i < amount_of_rockets; i++)
    rockets[i] = new rocket();
    
  asteroids = new asteroid[amount_of_asteroids];
  for (int i = 0; i < amount_of_asteroids; i++)
    asteroids[i] = new asteroid();
}

void draw()
{
  // Semi-transparent space background
  push();
  noStroke();
  fill(214, 80, 8, 70);
  rect(0, 0, width, height);
  pop();
  
  // Rockets update/display
  for (int i = 0; i < amount_of_rockets; i++)
  {
    rockets[i].update();
    rockets[i].display();
  }
  
  // Asteroids update/display
  for (int i = 0; i < amount_of_asteroids; i++)
  {
    asteroids[i].update();
    asteroids[i].display();
  }
}
