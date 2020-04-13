float x_off, y_off, z_off;
int scale;
int rows, cols;
int w = 2000;
int h = 2000;

float[][] z_vals;

float flying = 0;
PVector sunlight_dir;


void setup()
{
  size(900, 900, P3D);
  surface.setLocation(100, 50);
  colorMode(HSB, 360, 100, 100, 100);
  background(0);
  
  sunlight_dir = new PVector(0, 1, -0.1);
  directionalLight(64, 30, 100, sunlight_dir.x, sunlight_dir.y, sunlight_dir.z);

}

void draw()
{
    // Sun
  //pointLight(64, 30, 100, -width/2, 0, 100);
  sunlight_dir.x = mouseX - width/2;
  sunlight_dir.y = mouseY - width/2;
  sunlight_dir.normalize();
  directionalLight(64, 30, 100, sunlight_dir.x, sunlight_dir.y, sunlight_dir.z);
  
  scale = 30;
  rows = h / scale;
  cols = w / scale;
  
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
  
  fill(112, 50, 100);
  
  for (int y = 0; y < rows - 1; y++)
  {
    beginShape(TRIANGLE_STRIP);
    for (int x = 0; x < cols; x++)
    {
      // Fill mapped of Zheight for illusion of shading
      //fill(112, 50, map(z_vals[x][y], -300, 300, 0, 100));
      vertex(x * scale, y * scale, z_vals[x][y]);
      vertex(x * scale, (y + 1) * scale, z_vals[x][y+1]);
    }
    endShape();
  }
}
