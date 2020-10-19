class day_name_box_class
{
  float stroke_weight = DAY_NAME_OUTLINE_WEIGHT;
  float box_width = COL_SIZE + 1;
  float box_height = DAY_NAME_BOX_HEIGHT;
  int buffer_from_gridline_to_usable_space = 1;
  float inside_box_upper_left = stroke_weight/2 + buffer_from_gridline_to_usable_space;
  // 2 * buffer_from_gridline_to_usable_space because once for upper left corner, once for bottom right
  float inner_box_width = box_width - stroke_weight - (2 * buffer_from_gridline_to_usable_space);
  float inner_box_height = box_height - stroke_weight - (2 * buffer_from_gridline_to_usable_space);  
  
  PFont font = body_text_bold;
  int text_size = 14;
  String day_name = "";
  
  void display()
  {
    push();
      fill(360);
      noFill();
      stroke(0);
      // TODO: See if noStroke() gets rid of the need to adjust the box width and the inital translate for the first box
        // Colored lines?
      strokeWeight(1);
      
      rect(0, 0, box_width, box_height);

      noStroke();
      fill(360, 100, 100);
      rect(inside_box_upper_left, inside_box_upper_left, inner_box_width, inner_box_height);
    
      textFont(body_text_bold);
    
    pop();
  }
}
