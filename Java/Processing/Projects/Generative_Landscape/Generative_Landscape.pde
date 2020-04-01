float x_off, y_off, z_off;
int scale;
int rows, cols;
int w = 2000;
int h = 2000;

float[][] z_vals;

float flying = 0;


void setup()
{
  size(900, 900, P3D);
  colorMode(HSB, 360, 100, 100, 100);
  background(0);
  
  scale = 30;
  rows = h / scale;
  cols = w / scale;
  
}

void draw()
{
  flying -= 0.025;
  
  z_vals = new float[cols][rows];
  float y_off = flying;
  for (int y = 0; y < rows; y++)
  {
    float x_off = 0.0;
    for (int x = 0; x < cols; x++)
    {
      z_vals[x][y] = map(noise(x_off, y_off), 0, 1, -300, 300);
      
      x_off += 0.08;
    }
    y_off += 0.08;
  }
  
  background(color(200, 75, 100));
  //fill(color(277, 100, 25));
  //stroke(color(277, 100, 10));
  noStroke();
    
  translate(width/2, height/2);
  rotateX(PI/3);
  
  // Allows things to be drawn in the center of the window for rotateX(PI/3);
  translate(-w/2, -h/2);
  
  for (int y = 0; y < rows - 1; y++)
  {
    beginShape(TRIANGLE_STRIP);
    for (int x = 0; x < cols; x++)
    {
      fill(112, 50, map(z_vals[x][y], -300, 300, 0, 100));
      vertex(x * scale, y * scale, z_vals[x][y]);
      vertex(x * scale, (y + 1) * scale, z_vals[x][y+1]);
    }
    endShape();
  }
}
