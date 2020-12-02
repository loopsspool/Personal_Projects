// ART ALIGNMENT
String[] months_needing_margin_buffer = {"JANUARY", "MARCH", "MAY"};
int margin_buffer = 0;
float before_month_name_art_end_x;
float after_month_name_art_start_x;

float pixel_buffer_scale = 3;  // To retain image quality drawn on the buffer


// IMAGES
PImage leaf;


void month_art()
{
  potential_margin_adjust();
  draw_month_art();
}

void potential_margin_adjust()
{  
  // Adjusting size so text width is accurate
  textSize(MONTH_TEXT_SIZE);
  // Gets pixel-width of each character in phrase
  float text_width = textWidth(MONTH_AND_YEAR);
  
  // TODO: This may need adapting if month fonts change
  // Text width doesn't account for serifs, so this adjusts art margins accordingly
    // Only seems to affect a few months
  for (int i = 0; i < months_needing_margin_buffer.length; i++)
  {
    if (MONTH_NAME == months_needing_margin_buffer[i])
    {
      margin_buffer = 20;
      break;
    }
  }
  
  // Setting art end and start points, respectively
  before_month_name_art_end_x = ((width - text_width)/2) - margin_buffer;
  after_month_name_art_start_x = (width - (width - text_width)/2) + margin_buffer;
}

void draw_month_art()
{
  push();
    switch(MONTH_NAME)
    {
      case "SEPTEMBER":
        september_art();
        break;
      case "OCTOBER":
        october_art();
        break;
      case "NOVEMBER":
        november_art();
        break;
      case "DECEMBER":
        december_art();
        break;
    }
  pop();
}

void september_art()
{
  // Using a graphics buffer because theres a bug that tint doesn't show when exported to a pdf
    // There's also a scalar & scale call to retain image quality drawn on the buffer
  month_banner = createGraphics(ceil(width * pixel_buffer_scale), ceil(MONTH_BOX_HEIGHT * pixel_buffer_scale));
  
  month_banner.beginDraw();
    month_banner.colorMode(HSB, 360, 100, 100);
    
    // Background color
    month_banner.noStroke();
    month_banner.fill(202, 43, 100); // Blue sky
    month_banner.rect(0, 0, width * pixel_buffer_scale, MONTH_BOX_HEIGHT * pixel_buffer_scale);
    
    leaf = loadImage("leaf.png");
    month_banner.imageMode(CENTER);
    
    int leaf_size;
    float x, y;
    float rotation;
    int hue;
    int saturation;
    for (int i = 0; i < 2500; i++)
    {
      month_banner.push();
        // Randomizing leaf elements
        leaf_size = ceil(random(20, 50) * pixel_buffer_scale);
        x = random(-leaf_size, (width * pixel_buffer_scale) + leaf_size);
        y = random(-leaf_size, MONTH_BOX_HEIGHT * pixel_buffer_scale);
        month_banner.translate(x, y);
        rotation = radians(random(360));
        hue = ceil(random(0, 50));
        saturation = ceil(random(70, 90));
        
        // Drawing the leaves
        month_banner.rotate(rotation);
        month_banner.tint(hue, saturation, 100);
        month_banner.image(leaf, 0, 0, leaf_size, leaf_size);
      month_banner.pop();
    }
  month_banner.endDraw();
  
  push();
    scale(1/pixel_buffer_scale, 1/pixel_buffer_scale);
    image(month_banner, 0, 0);
  pop();
  
  
  // MONTH NAME
  font_class sept_font = new font_class();
  
  sept_font.font = default_month_font;
  sept_font.size = MONTH_TEXT_SIZE;
  sept_font.fill = color(0);
  sept_font.text = MONTH_AND_YEAR;
  sept_font.x = width/2;
  sept_font.y = MONTH_BOX_HEIGHT/1.4;
  sept_font.is_outlined = true;
  sept_font.outline_color = color(360);
  sept_font.outline_weight = .5;
  sept_font.is_bolded = true;
  sept_font.bold_weight = 6;
  
  draw_text(sept_font);
}

void october_art()
{ 
  month_banner = createGraphics(width, int(MONTH_BOX_HEIGHT));

  class Spiderweb
  {
    float origin_x;
    float origin_y;
    
    Spiderweb(float x, float y)
    {
      origin_x = x;
      origin_y = y;
    }
    
    void display()
    {
      push();
            month_banner.translate(origin_x, origin_y);
            month_banner.stroke(360);
            month_banner.noFill();
            month_banner.strokeWeight(3);
            int circle_d = 30;
            month_banner.circle(0, 0, circle_d);
            
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
                month_banner.rotate(rotation);
                month_banner.line(0, -circle_d/2, 0, -width);
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
                month_banner.rotate(rotation_array[i]);
                push();
                  // Puts axis halfway between current main line and next
                    // Negated by pop(), so will hop back to current main line so rotate will be accurate still
                  month_banner.rotate(rotation_array[i+1]/2);
                  month_banner.translate(0, -circle_d/2);
                  
                  // The below method works
                    // Only drawback is get() will go offscreen after rotate call
                      // This means it'll always return black, resulting in an infinite loop
                        // Tho could do an arc amount check and after it gets to a certain number
                          // Add 25. x looks close to adding 20 + (loop_acc * 4)
                  int y_base = 0;
                  int y_inc = 0;  // Changes the incrementer value so it doesn't look so "perfect"
                  int loop_acc = 0;
                  for (int y = -y_base; y > -height * 1.5; y -= y_base + y_inc)
                  {
                    int x = 0;
                    while(month_banner.get(int(screenX(x, y)), int(screenY(x, y))) == color(0))
                    {
                      x++;
                    }
                    //x += 20 + (4 * loop_acc);
                    //println(x);
          
                    month_banner.stroke(360);
                    month_banner.beginShape();
                      // First and fifth vertices are control points
                      month_banner.curveVertex(-x, y);
                      month_banner.curveVertex(-x, y);
                      month_banner.curveVertex(0, y * 0.8);
                      month_banner.curveVertex(x, y);
                      month_banner.curveVertex(x, y);
                    month_banner.endShape();
                    
                    y_inc += 10;
                    loop_acc++;
                  }
                pop();
              }
            }
        pop();  
        }
  }
  
  noStroke();
  fill(0);
  rect(0, 0, width, MONTH_BOX_HEIGHT);
  Spiderweb ul_spiderweb = new Spiderweb(0, 0);
  Spiderweb lr_spiderweb = new Spiderweb(width - 1, MONTH_BOX_HEIGHT);
  month_banner.beginDraw();
    month_banner.colorMode(HSB, 360, 100, 100);
    month_banner.background(0);
    ul_spiderweb.display();
    lr_spiderweb.display();
  month_banner.endDraw();
  
  image(month_banner, 0, 0);
}

void november_art()
{
  fill(200);
  rect(0, 0, width, MONTH_BOX_HEIGHT);
  
  for (int i = 0; i < 300; i++)
  {
    stroke(random(220, 300));
    float start_x = random(-50, width);
    float start_y = random(-50, MONTH_BOX_HEIGHT);
    float drop_length = random(10, 100);
    line(start_x, start_y, start_x + drop_length, start_y + drop_length + random(-5));
  }
  
  // MONTH NAME
  font_class nov_font = new font_class();
 
  nov_font.font = new RFont("data\\COOPBL.TTF", 60, RFont.CENTER);
  nov_font.size = MONTH_TEXT_SIZE;
  nov_font.fill = color(0);
  nov_font.text = MONTH_AND_YEAR;
  nov_font.x = width/2;
  nov_font.y = MONTH_BOX_HEIGHT/1.4;
  nov_font.is_outlined = true;
  nov_font.outline_color = color(0);
  nov_font.outline_weight = 3;
  nov_font.is_bolded = false;
  nov_font.is_layered = true;
  nov_font.layers_are_outlined = true;
  nov_font.layer_colors = new int[] {color(0), color(119, 45, 84), color(288, 100, 90), color(189, 43, 94)};
  
  draw_text(nov_font);
}

void december_art()
{
  // TODO: Restrict positioning to not overlap other snowflakes
  month_banner = createGraphics(ceil(width * pixel_buffer_scale), ceil(MONTH_BOX_HEIGHT * pixel_buffer_scale));
  final color background_color = color(202, 43, 100);
  
  class Snowflake
  {
    float x = random(0, width * pixel_buffer_scale);
    float y = random(0, MONTH_BOX_HEIGHT * pixel_buffer_scale);
    
    // Core features
    float random_rotation = radians(random(100, 300));
    int amount_of_arms = int(random(5, 10));
    float arm_degrees = radians(360/amount_of_arms);
    int arm_min = 5;
    int arm_max = 15;
    int arm_length = int(random(arm_min, arm_max) * pixel_buffer_scale);
    int amount_of_fingers = int(random(2, 5));
    float finger_degrees = radians(180/amount_of_fingers);
    
    // Extra features
    // TODO: Implement these!
    boolean has_webs = random_boolean();
    int amount_of_webs = int(random(0, 5));
    boolean has_hairs = random_boolean();
    int amount_of_hairs = int(random(3, 6));
    boolean has_ngon_base = random_boolean();
    boolean base_has_solid_fill = random_boolean();
    boolean has_multiple_ngons = random_boolean();
    int amount_of_ngons = int(random(1, 5));
    boolean has_star_base = random_boolean();
    boolean has_multiple_stars = random_boolean();
    int amount_of_stars = int(random(1, 5));
    float base_distance = random(3, arm_length/5);  // Distance from origin where base is
    
    void set_positioning()
    {
      month_banner.translate(x, y);
      // Randomly rotating the snowflake for realism of falling snowflakes
      month_banner.rotate(random_rotation);
    }
    
    void arms()
    {
      month_banner.line(0, 0, 0, arm_length);
    }
    
    void fingers()
    {
      month_banner.push();
        month_banner.translate(0, arm_length);
        // Centered positioning of the fingers is dependent on the starting angle of the rotations
          // This changes with how many fingers there are, so the below functionn calculates it
        float finger_degree_initializer = radians(((amount_of_fingers - 1) * degrees(finger_degrees))/2 - 180);
        // Initializes starting rotation point for fingers to build rotation
        month_banner.rotate(finger_degree_initializer);
        
        for (int i = 0; i < amount_of_fingers; i++)
        {
          // Building rotation at each finger
          month_banner.rotate(finger_degrees);
          month_banner.line(0, 0, 0, 5 * pixel_buffer_scale);
        }
      month_banner.pop();
    }
    
    void webbing()
    {
      month_banner.push();
        if (has_webs)
        {
          // Rotating in between the arms so lines across can be calculated cleanly
          month_banner.rotate(arm_degrees/2);
          // Starting at 1 so web lines aren't drawn at origin (bc multiplied by 0
          for (int i = 1; i < amount_of_webs + 1; i++)
          {
            // To kind of equal out the webbing...
              // Subtract 1 from arm_length until % 16 == 0
              // Figure out how to find x (3/4 of y?)
            
            // Using 4 and 3s for bases because those are perfect right triangles
            // The webs between the arms create an isocoles triangle from the origin point
              // But going from the middle of the arms this can be seen as two equal right triangle
            float web_y = 4 * i;
            float web_x = 3 * i;
            
            // I don't know why I have to multiply arm length by 1/2
              // If I don't the webbing will extend on some well beyond the snowflake
            if (web_y < (arm_length * 1/2))
            {
              month_banner.translate(0, web_y);
              month_banner.line(-web_x, 0, web_x, 0);
            }
          }
        }
      month_banner.pop();
    }
    
    void hairs()
    {
      // Snowflake hairs
      // TODO: If snowflake looks too much a ball can adjust parameters (hair based off size?) here
      month_banner.push();
        if (has_hairs)
        {
          float hair_spacing = arm_length/amount_of_hairs;
          // Initializes first hair distance from origin
          float hair_y = hair_spacing;
          float hair_length = map(arm_length, arm_min, arm_max, 1, 4) * pixel_buffer_scale;

          // TODO: Change angle of hairs?
          for (int m = 0; m < amount_of_hairs; m++)
          {
            month_banner.translate(0, hair_y);
            month_banner.push();
              month_banner.rotate(radians(-45));
              month_banner.line(0, 0, 0, hair_length);
              month_banner.rotate(radians(90));
              month_banner.line(0, 0, 0, hair_length);
            month_banner.pop();
          }
        }
      month_banner.pop();
    }
    
    void ngon_base()
    {
      month_banner.push();
        if (has_ngon_base)
        {
          if (base_has_solid_fill)
            month_banner.fill(background_color);
          else 
            month_banner.noFill();
          
          if (!has_multiple_ngons)
          {
            month_banner.beginShape();
              // Keeping this at amount_of_arms + 2 draws over the final snowflake arm
                // That has a chance of drawing over the ngon
              for (int m_ = 1; m_ < amount_of_arms + 2; m_++)
              {
                float x_ = base_distance * sin(arm_degrees * m_) * pixel_buffer_scale;
                float y_ = base_distance * cos(arm_degrees * m_) * pixel_buffer_scale;
                
                month_banner.vertex(x_, y_);
              }
            month_banner.endShape(CLOSE);
          }
          else
          {
            
          }
        }
      month_banner.pop();
    }
    
  }
  
  int snowflake_count = 25;
  Snowflake[] snowflakes = new Snowflake[snowflake_count];
  
  for (int i = 0; i < snowflake_count; i++)
  {
    snowflakes[i] = new Snowflake();
    
    // Verifies no snowflakes overlap one another
      // If this turns out so slow you can devise a grid for the banner with units as large as the biggest snowflake. 
      // Snowflake positions will be selected on this grid and when one is theat square can no longer have the chance of being selected
      // One snowflake per grid square. Once filled, that square cannot be chosen again
    int i_ = i - 1;  // Checks the most recent snowflake
    float snowflake_buffer = 15;
    while (i_ >= 0)
    {
      // If the distance between the origin of the two snowflakes is smaller than the sum of their radius
        // Give then new coordinates
      if (dist(snowflakes[i].x, snowflakes[i].y, snowflakes[i_].x, snowflakes[i_].y) < (snowflakes[i].arm_length + snowflakes[i_].arm_length + snowflake_buffer))
      {
        // Resets coordinates
        snowflakes[i].x = random(0, width * pixel_buffer_scale);
        snowflakes[i].y = random(0, MONTH_BOX_HEIGHT * pixel_buffer_scale);
        // Resets index to most recent element to re-check all made snowflakes with new coordinates
        i_ = i - 1;
      }
      else
        i_ -= 1;  // Checks next snowflake coordinates
    }
  }
  
  // Actually drawing the snowflakes
  month_banner.beginDraw();
    month_banner.colorMode(HSB, 360, 100, 100, 100);
    
    month_banner.push();
      // BACKGROUND
      month_banner.noStroke();
      month_banner.fill(background_color);
      month_banner.rect(0, 0, width * pixel_buffer_scale, MONTH_BOX_HEIGHT * pixel_buffer_scale);

      // SNOWFLAKE DRAWING
      month_banner.stroke(360);
      month_banner.strokeWeight(3);
      for (int i = 0; i < snowflakes.length; i++)
      {
        month_banner.push();
        snowflakes[i].set_positioning();
          for (int i_ = 0; i_ < snowflakes[i].amount_of_arms; i_++)
          {
            // Rotates to each arm for each function
            month_banner.rotate(snowflakes[i].arm_degrees);
            snowflakes[i].arms();
            snowflakes[i].fingers();
            snowflakes[i].webbing();
            snowflakes[i].hairs();
            snowflakes[i].ngon_base();
          }
        month_banner.pop();
      }
      
    month_banner.pop();
  month_banner.endDraw();
  
  push();
    scale(1/pixel_buffer_scale, 1/pixel_buffer_scale);
    image(month_banner, 0, 0);
  pop();
  
}

boolean random_boolean()
{
  return Math.random() < 0.5;
}

  // CODE FOR ONLY DRAWING AROUND THE NAME, NOT FULL BANNER
  //noStroke();
  //fill(360);
  //rect(0, 0, before_month_name_art_end_x, MONTH_BOX_HEIGHT);
  //rect(after_month_name_art_start_x, 0, width, MONTH_BOX_HEIGHT);
