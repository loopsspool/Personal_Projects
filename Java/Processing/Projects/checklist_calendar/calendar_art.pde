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
  leaf = loadImage("leaf.png");
  
  tint(23, 100, 100);
  image(leaf, width/2, height/2);
  //noStroke();
  //fill(360);
  //rect(0, 0, before_month_name_art_end_x, MONTH_BOX_HEIGHT);
  //rect(after_month_name_art_start_x, 0, width, MONTH_BOX_HEIGHT);
  

}
