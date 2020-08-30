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
