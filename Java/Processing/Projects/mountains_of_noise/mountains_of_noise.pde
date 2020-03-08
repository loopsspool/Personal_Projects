mountain[] mountains;

void setup()
{
  size(800, 800);
  colorMode(HSB, 360, 100, 100);
  background(270, 100, 26);
  
  int amount_of_mountains = 6;
  mountains = new mountain[amount_of_mountains];
  
  // TODO: Set color gradient based on what mountain range it is
    // (farther back lighter, closer darker colors)
  for (int i = 0; i < amount_of_mountains; i++)
  {
    float mountain_y_start = map(i, 0, amount_of_mountains, 150, 7 * height/8);
    mountains[i] = new mountain(mountain_y_start);
    mountains[i].build_mountain();
    mountains[i].display();
  }
}

void draw()
{

}
