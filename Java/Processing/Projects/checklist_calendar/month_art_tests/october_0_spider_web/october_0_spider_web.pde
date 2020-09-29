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
      float amount_of_arcs = 20;
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
          int x = 0;
          int x_add;
          
          // The below method works
            // Only drawback is get() will go offscreen after rotate call
              // This means it'll always return black, resulting in an infinite loop
                // Tho could do an arc amount check and after it gets to a certain number
                  // Add 25. x looks close to adding 20 + (loop_acc *5)
          int y_base = 30;
          int y_inc = 10;
          int loop_acc = 0;
          for (int y = -y_base; y > -height; y -= y_base + y_inc)
          {
            x = 0;
            while(get(int(screenX(x, y)), int(screenY(x, y))) == color(0))
            {
              x++;
            }
            println(x);
            // x = 20 + (loop_acc * 5);
  
            stroke(360);
            beginShape();
              // First and fifth vertices are control points
              curveVertex(-x, y);
              curveVertex(-x, y);
              curveVertex(0, y * 0.8);
              curveVertex(x, y);
              curveVertex(x, y);
            endShape();
            
            y_inc += 10;
            loop_acc++;
          }
          
          
          
          // ALMOST WORKS
          //for (int i_ = 0; i_ < amount_of_arcs; i_++)
          //{
          //  y += pow(1.3, i_);
            
          //  translate(0, -y);
          //  // x still doesn't quite reach to the edge of the main lines
          //  x = (y * (sin(inside_angle))/sin(radians(90) - inside_angle)) + ((i_ + 2) * y/9);
  
          //  stroke(360);
          //  beginShape();
          //    // First and fifth vertices are control points
          //    curveVertex(-x, 0);
          //    curveVertex(-x, 0);
          //    curveVertex(0, y/10);
          //    curveVertex(x, 0);
          //    curveVertex(x, 0);
          //  endShape();
          //}
        pop();
      }
    }
    
    // DOESN'T WORK
    //PShape arc;
    //arc = createShape();
    //arc.setStroke(#EA2FEA);
    //for (int i = 0; i < main_strings - 1; i++)
    //{
    //  arc.rotate(rotation_array[i]);
    //  push();
    //    arc.beginShape();
          
    //      arc.curveVertex(0, -150);
    //      arc.curveVertex(0, -150);
    //      arc.rotate(rotation_array[i+1]/2);
    //      arc.curveVertex(10, -100);
    //      arc.rotate(rotation_array[i+1]/2);
    //      arc.curveVertex(0, -150);
    //      arc.curveVertex(0, -150);
    //    arc.endShape(CLOSE);
    //  pop();
    //}
    //shape(arc);
    
  pop();
}
