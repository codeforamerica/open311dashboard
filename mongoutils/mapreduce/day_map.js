function day_map(){
  try{
    emit(this.requested_datetime.split('T')[0], {count : 1});
  } catch (error) { 
    return ;
  }
}
