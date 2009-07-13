//$.post("/courses/course/topic/questions/",	{'url': '/courses/course/topic/ENTPR/12'},	function(data) {$("div#questions").text(data);});
/*
function get_questions() {
		$.getJSON("/courses/course/topic/questions/?url=/courses/course/topic/ENTPR/12", function(data) {
		$.each(data, function(i, item) {
			if(item.error) {
				alert('This was an error while processing this page');
			}
			$("div#questions").append("<p><a href='javascript:question_clicked()'>" + item.fields.text + "</a></p>");
		});
	});
	setInterval(get_questions(), 10000)
};
*/
//get_questions();
function contains(obj, element) {
	var i =0;
	for(i=0;i<obj.length;i++) {
		if(obj[i] == element) {
			return true;
		}
	}
	return false;
}

var questions = {};
$("div#questions").poll({
    url: "/courses/course/topic/questions/?url=" + window.location.pathname,
    success: function(data){
			$.each(data, function(i, item) {
				if(item.error) {
					alert('This was an error while processing this page');
				}
				else {
					if(!(item.pk in questions)) {
						questions[item.pk] = item.fields.text;
						$("div#questions").append("<p><a href='javascript:question_clicked(" + item.pk + ")'>" + item.fields.title + "</a></p>");
					}
				}
			});
    }
});

