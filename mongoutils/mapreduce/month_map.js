function month_map(){
  try{
    emit(this.requested_datetime.slice(0,7), {count : 1});
  } catch (error) { 
    return ;
  }
}
