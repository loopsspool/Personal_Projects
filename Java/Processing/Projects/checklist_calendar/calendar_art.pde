// ART ALIGNMENT
String[] months_needing_margin_buffer = {"JANUARY", "MARCH", "MAY"};
int margin_buffer = 0;
float before_month_name_art_end_x;
float after_month_name_art_start_x;

// IMAGES
PImage leaf;

// TODO: Allow full-width art (0, width)(includes text)

void month_art()
{
  potential_margin_adjust();
  draw_month_art();
}

void potential_margin_adjust()
{  
  // Adjusting size so text width is accurate
  textSize(MONTH_TEXT_SIZE);
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
    }
  pop();
}

void september_art()
{
  // TODO: Leaf image quality is bad
  
  september_banner = createGraphics(width, ceil(MONTH_BOX_HEIGHT));
  september_banner.beginDraw();
  september_banner.colorMode(HSB, 360, 100, 100);
  
  // Background color
  september_banner.noStroke();
  september_banner.fill(202, 43, 100); // Blue sky
  september_banner.rect(0, 0, width, MONTH_BOX_HEIGHT);
  
  leaf = loadImage("leaf.png");
  september_banner.imageMode(CENTER);
  
  int leaf_size;
  float x, y;
  float rotation;
  int tint;
  for (int i = 0; i < 2500; i++)
  {
    september_banner.push();
      // Randomizing leaf elements
      leaf_size = ceil(random(20, 50));
      x = random(-leaf_size, width + leaf_size);
      y = random(-leaf_size, MONTH_BOX_HEIGHT);
      september_banner.translate(x, y);
      rotation = radians(random(360));
      tint = ceil(random(0, 60));
      
      // Drawing the leaves
      september_banner.rotate(rotation);
      september_banner.tint(tint, 100, 100);
      september_banner.image(leaf, 0, 0, leaf_size, leaf_size);
    september_banner.pop();
  }

  september_banner.endDraw();
  image(september_banner, 0, 0);

  // CODE FOR ONLY DRAWING AROUND THE NAME, NOT FULL BANNER
  //noStroke();
  //fill(360);
  //rect(0, 0, before_month_name_art_end_x, MONTH_BOX_HEIGHT);
  //rect(after_month_name_art_start_x, 0, width, MONTH_BOX_HEIGHT);
  
  // MONTH NAME
  fill(0);
  textFont(august_month_font);
  textSize(MONTH_TEXT_SIZE);
  // "Bolds" the font a little -- since theres no bold version
  for (int i = 0; i < 2; i++)
    text(MONTH_AND_YEAR, (width/2) + i, MONTH_BOX_HEIGHT/2.3);
}
