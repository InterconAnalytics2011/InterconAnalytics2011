var words = [];

jQuery(document).ready(function() {
	jQuery.ajax({
        url: '/data/keywords',
		context: document.body,
        success: function(data){
			for(var i = 0; i < data.feed.length; i++) {
				words[i] = {text: data.feed[i].keyword, weight: data.feed[i].visits};
			}
        }
    });
});
