jQuery(document).ready(function($) {

  if (window.history && window.history.pushState) {

    $(window).on('popstate', function() {
      var hashLocation = location.hash;
      var hashSplit = hashLocation.split("#!/");
      var hashName = hashSplit[1];

      if (hashName !== '') {
        var hash = window.location.hash;
        if (hash === '') {
          alert('Back button was pressed.');
        }
      }
    });

    window.history.pushState('forward', null, './');
  }

});


$(function(){
    //Changes chart type in graph
    jQuery('#chartType').on('change', function(){
        var chartType = $(this).val();
        var figureID = $(this).parents('div').attr('id');
        var json_file_path = $('#json_file-path').val();
        generateHighChartTS(json_file_path,figureID,chartType); 
    });

});
