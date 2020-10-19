public class font_class
{
  // FONT INFO
  RFont font = default_month_font;
  int size = MONTH_TEXT_SIZE;
  color fill = color(0);
  String text = "default";
  float x = width/2;
  float y = MONTH_BOX_HEIGHT/1.4;
  
  // EFFECTS INFO
  boolean is_outlined = false;
  color outline_color = color(360, 100);
  float outline_weight = 0.2;
  
  boolean is_bolded = false;
  int bold_weight = 2;
  
  void set_features()
  {
    font.setSize(size);
    fill(fill);
    
    if (is_outlined)
    {
      strokeWeight(outline_weight);
      stroke(outline_color);
    }
    else
      noStroke();
    
    translate(x, y);
  }
  
  void display()
  {
    font.draw(text);
  }
}

void draw_text(font_class Font)
{
  push();
    if (Font.is_bolded)
      bold_font(Font);
    else
    {
      Font.set_features();
      Font.display();
    }
  pop();
}

void bold_font(font_class Font)
{
  push();
    Font.set_features();
    // "Bolds" the font a little -- since theres no bold versions of some fonts
    float x_shift_divisor = 5;  // To utilize i as coordinate, small shifts in x
    for (float i = 0; i < Font.bold_weight/x_shift_divisor; i += 1/x_shift_divisor)
    {
      translate(i, 0);
      Font.display();
    }
  pop();
}

/** 
TODO: Text effects: 
  - 3D gradually increasing font size
  - Text Fade in/out
  + See what geomerative can do
  
  Maybe make its own tab?
**/ 
