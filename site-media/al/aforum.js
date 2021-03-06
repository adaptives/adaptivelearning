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

var questions = {};

function update_questions(data) {
	$.each(data, function(i, item) {
		if(item.error) {
			alert('This was an error while processing this page');
		}
		else {
			if(!(item.pk in questions)) {
				questions[item.pk] = item.fields.text.replace(/\n/g, '<br>');
				$("div#questions").append("<p id='" + item.pk + "'><a href='javascript:question_clicked(" + item.pk + ")'>" + item.fields.title + "</a> <i>asked about " + item.fields.time_asked + " ago by - <a href='/profile/public/" + item.fields.user + "/'>" + item.fields.user + "</i> </a></p>");
			}
		}
	});
}

$.getJSON("/dtforum/questions/?url=" + window.location.pathname, function(data) {
	update_questions(data);
});

$("div#questions").poll({
    url: "/dtforum/questions/?url=" + window.location.pathname,
    success: function(data){
			/*
			$.each(data, function(i, item) {
				if(item.error) {
					alert('This was an error while processing this page');
				}
				else {
					if(!(item.pk in questions)) {
						questions[item.pk] = item.fields.text;
						$("div#questions").append("<p id='" + item.pk + "'><a href='javascript:question_clicked(" + item.pk + ")'>" + item.fields.title + "</a></p>");
					}
				}
			});
			*/
			update_questions(data);
    }
});

