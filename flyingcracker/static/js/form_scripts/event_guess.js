$(function(){

  /* Set Competitor selections */
  function setCompetitors(id_list) {
    if (id_list != '') {
      var arr = id_list.split(',');
      $("select[name|='form'][name$='competitor']").each(function(k,v){
        if (arr.length > 0) {
          $(v).val(arr.pop());
        }
        else {
          $(v).val('');
        }
      });
    }
  }
  
  // ============
  // = Triggers =
  // ============

  // Team selection changed
  $("#id_team").change(function(){
    setCompetitors($(this).val());
  });

  // Competitor selection changed
  $("select[name|='form'][name$='competitor']").change(function(){
    $("#id_team").val('');
  });

});