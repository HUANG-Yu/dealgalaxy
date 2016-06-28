function draw_line_graph() {
    
    $.post(
        '/blank-page/getcashback',
        {
            'websitename': websitename,
        },
        function(data) {
            Morris.Line({
            element: 'line-example',
            data: data.result
            xkey: 'crawldate',
            ykeys: ['cashback'],
            labels: ['Cash Back Percentage']
        }
    );
}