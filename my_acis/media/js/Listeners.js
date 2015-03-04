$(function(){
    //Changes chart type in graph
    jQuery('#chartType').on('change', function(){
        console.log('YO')
        var chartType = $(this).val();
        var figureID = $(this).parents('div').attr('id');
        var json_file_path = $('#json_file-path').val();
        generateHighChartTS(json_file_path,figureID,chartType); 
    });

});
