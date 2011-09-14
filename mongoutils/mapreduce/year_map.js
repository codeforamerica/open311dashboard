function year_map(){
  try{
    emit(this.requested_datetime.slice(0,4), {count : 1});
  } catch (error) { 
    return ;
  }
}
