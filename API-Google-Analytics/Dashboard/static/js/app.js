/* config vars */
var dash = dash || {};
dash.current_slide = 1; // keep reference of current slide
dash.slide_count = 2; // total slide numbe

// Ready
jQuery(function(){
    jQuery(document).keydown(function(event) {
		if (event.keyCode == '39') {
			rotate_slide('next');	
		}
		if (event.keyCode == '37') {
			rotate_slide('previous');
		}
	});
		
	jQuery('#paging-left').mousedown(function() {
		jQuery(this).removeClass('paging-left-inactive').addClass('paging-left-active');
	}).mouseup(function() {
		jQuery(this).removeClass('paging-left-active').addClass('paging-left-inactive');
		rotate_slide('previous');
	});
		
	jQuery('#paging-right').mousedown(function() {
		jQuery(this).removeClass('paging-right-inactive').addClass('paging-right-active');
	}).mouseup(function() {
		jQuery(this).removeClass('paging-right-active').addClass('paging-right-inactive');
		rotate_slide('next');
	});
});

// Rotate slide
var rotate_slide = function(button){
	jQuery('#slide-' + dash.current_slide).fadeOut('slow',function(){

        if(button == 'previous'){
            if(dash.current_slide <= 1){
                dash.current_slide = dash.slide_count;
            }else{
                dash.current_slide = dash.current_slide - 1;
            }
        }else{
            if(dash.current_slide >= dash.slide_count){
                dash.current_slide = 1;
            }else{
                dash.current_slide = dash.current_slide + 1;
            }
        }
        
        jQuery('#slide-' + dash.current_slide).fadeIn('slow');
        
        if(dash.current_slide == 2){
            jQuery('#tag-cloud').jQCloud(words, {randomClasses: 10});
        }else{
            jQuery('#tag-cloud').html('');
        }
    });
}	

// Rotate slide every 2 minutes
setInterval(rotate_slide, 1000 * 60 * 1, 'next');

// fully reload page every 12 hours
// avoid session timeout, and keep it updated if running idefinitely
setTimeout('window.location.reload()', 1000 * 60 * 60 * 12);