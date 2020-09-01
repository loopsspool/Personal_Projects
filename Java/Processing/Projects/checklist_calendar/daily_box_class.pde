public class daily_box_class
{
  float box_width = COL_SIZE;
  float box_height = ROW_SIZE;
  int day_number = 0;
  String[] check_off_items = {"Do morning routine", 
                              "Be present", 
                              "Do thing you love", 
                              "Spend time w/ self", 
                              "Do list"};

  void display(int day_num)
  {
    push();
      fill(360);
      noFill();
      stroke(0);
      strokeWeight(1);
      
      rect(0, 0, COL_SIZE, ROW_SIZE);
      stroke(180);
      line(2, 0, 2, ROW_SIZE);
      line(COL_SIZE - 2, 0, COL_SIZE -2, ROW_SIZE);
    
    pop();
  }
}
