class day_name_box_class
{
  float box_width = COL_SIZE;
  float box_height = DAY_NAME_BOX_HEIGHT;
  int stroke_weight = DAY_NAME_OUTLINE_WEIGHT;
  PFont font = body_text_bold;
  int text_size = 14;
  
    void display()
  {
    push();
      fill(360);
      noFill();
      stroke(0);
      strokeWeight(stroke_weight);
      
      rect(0, 0, box_width, box_height);

      noStroke();
      fill(360, 100, 100);
      rect(stroke_weight, stroke_weight, box_width - (2 * stroke_weight), box_height - (2 * stroke_weight));
    
    pop();
  }
}
