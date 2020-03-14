// Asteroids plow through space carried solely by the momentum

class asteroid
{
  PImage asteroid_img;
  float rotation;
  float rotation_acc;
  
  PVector acceleration;
  PVector velocity;
  PVector location;
  
  float top_speed;
  
  asteroid()
  {
    asteroid_img = loadImage("Asteroid.png");
    top_speed = random(3, 5);
    
    float x_decider = random(-1, 1);  // Decides if asteroid will move left or right
    float y_decider = random(-1, 1);  // Decides if asteroid will move up or down
    location = new PVector(random(width), random(height));
    velocity = new PVector(0, 0);  

    if (x_decider >= 0)
    {
      if (y_decider >= 0)
        acceleration = new PVector(random(0.25, 4), random(1, 3));
      else
        acceleration = new PVector(random(0.25, 4), random(-1, -3));
    }
    else
    {
      if (y_decider >= 0)
        acceleration = new PVector(random(-0.25, -4), random(1, 3));
      else
        acceleration = new PVector(random(-0.25, -4), random(-1, -3));
    }
    
    rotation = 0;
    rotation_acc = radians(random(-1, 1));
  }
  
  void check_edges()
  {
    if (location.x > width)
      location.x = 0;
    if (location.x < 0)
      location.x = width;
      
    if (location.y > height)
      location.y = 0;
    if (location.y < 0)
      location.y = height;
  }

  void update()
  {
    velocity.add(acceleration);
    velocity.limit(top_speed);
    location.add(velocity);
    
    rotation += rotation_acc;
    
    check_edges();
  }
  
  void display()
  {
    push();
    translate(location.x, location.y);
    rotate(rotation);
    image(asteroid_img, 0, 0, 80, 80);
    pop();
  }
}
