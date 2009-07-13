/*
 *Source: http://buntin.org/2008/sep/23/jquery-polling-plugin/
 */
(function($) {
    $.fn.poll = function(options){
        var $this = $(this);
        //extend our default options with those provided
        var opts = $.extend({}, $.fn.poll.defaults, options);
        setInterval(update, opts.interval);
        // method used to update element html
        function update(){
        	$.ajax({
        		type: opts.type,
						dataType: opts.dataType,
            url: opts.url,
            success: opts.success
        	});
        };
    };
    // default options
    $.fn.poll.defaults = {
    	type: "GET",
    	url: ".",
      success: '',
      interval: 5000,
			dataType: 'json'
    };
})(jQuery);

