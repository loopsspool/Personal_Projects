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
        // Adds a bit of randomness but makes it difficult to work around
        //rotation = radians(360/(main_strings + random(-4, 4)));
        rotation = radians(360/main_strings);
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
            // Negated by pop(), so will hop back to current main line so rotate will be accurate still
          rotate(rotation_array[i+1]/2);
          translate(0, -circle_d/2);
          // Middle test line
          //stroke(#EA2FEA);
          //line(0, 0, 0, -height);
          float x = 0;
          float y = 0;
          float inside_angle = rotation_array[i+1]/2;

          // Maybe instead of rotating to the half of each line, draw the arcs with
            // No rotate calls, just using sin and cosine
          float amount_of_arcs = 20;
          float half_diagonal = sqrt(sq(width) + sq(height))/2;
          
          for (int i_ = 0; i_ < amount_of_arcs; i_++)
          {
            y += pow(1.3, i_);
            
            translate(0, -y);
            // x still doesn't quite reach to the edge of the main lines
            x = (y * (sin(inside_angle))/sin(radians(90) - inside_angle)) + ((i_ + 2) * y/9);
  
            stroke(360);
            beginShape();
              // First and fifth vertices are control points
              curveVertex(-x, 0);
              curveVertex(-x, 0);
              curveVertex(0, y/10);
              curveVertex(x, 0);
              curveVertex(x, 0);
            endShape();
          }
        pop();
      }
    }
  pop();
}
