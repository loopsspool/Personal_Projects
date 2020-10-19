public class daily_box_class
{
  float stroke_weight = DAY_GRID_STROKE_WEIGHT;

  float box_width = COL_SIZE;
  float box_height = ROW_SIZE;
  int buffer_from_gridline_to_usable_space = 1;
  float inside_box_upper_left = stroke_weight/2 + buffer_from_gridline_to_usable_space;
  // 2 * buffer_from_gridline_to_usable_space because once for upper left corner, once for bottom right
  float inner_box_width = box_width - stroke_weight - (2 * buffer_from_gridline_to_usable_space);
  float inner_box_height = box_height - stroke_weight - (2 * buffer_from_gridline_to_usable_space);
  
  int day_number = 0;
  String[] check_off_items = {"Do morning routine", 
                              "Be present", 
                              "Do thing you love", 
                              "Spend time w/ self", 
                              "Do list"};

  void display(int day_num)
  {
    push();   
      stroke(0);
      strokeWeight(stroke_weight);
      
      day_number = day_num;
      
      if (day_number == 0 || day_number > DAYS_IN_MONTH)
      {
        fill(280);
        rect(0, 0, box_width, box_height);
      }
      else
      {
        fill(360);
        rect(0, 0, box_width, box_height);
        
        numbers();
        checklist();
        done_today_checkbox();
      }
      
      // INSIDE BOX TEST
      //noStroke();
      //fill(360, 100, 100);
      //rect(inside_box_upper_left, inside_box_upper_left, inner_box_width, inner_box_height);
    
    pop();
  }
  
  void numbers()
  {
    push();
      translate(4, 8);
      textAlign(LEFT, CENTER);
      textFont(body_text_bold);
      textSize(12);
      stroke(0);
      fill(0);
      text(String.valueOf(day_number), 0, 0);
    pop();
  }
  
  void checklist()
  {
    float indent = 13;
    float size = 9.4;
    float y_translate = 0;
    // Adjusting for rows of calendar so alignment doesn't look funky
    // TODO: Align to liking
    if (AMOUNT_OF_ROWS == 6)
      y_translate = 11.7;
    if (AMOUNT_OF_ROWS == 5)
      y_translate = 14.5;
    if (AMOUNT_OF_ROWS == 4)
      y_translate = 18;
    
    push();
      textFont(body_text);
      
      translate(7, 7);
      for (int i = 0; i < check_off_items.length; i++)
      {
        translate(0, y_translate);
        noFill();
        strokeWeight(1);
        square(0, 0, size);
        textSize(size);
        textAlign(LEFT);
        fill(0);
        text(check_off_items[i], indent, 0.9 * size);
      }
    pop();
  }
  
  void done_today_checkbox()
  {
    push();
      rectMode(CENTER);
      noFill();
      strokeWeight(1);
      // Matches checkbox items square size
      float square_size = 9.4;
      // -1 on x and +8 on y to align with day numbers
      square(box_width - square_size - 1, square_size/4 + 8, square_size);
    pop();
  }
}
