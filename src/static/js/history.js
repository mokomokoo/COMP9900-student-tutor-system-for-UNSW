// fix indent of the question
$("#sub").click(function(){	
	$.ajax({
		url: "/history",
		type: "POST",
		data: {
			'question':$("#question").val(),
			'description':$("#description").val(),
		},
		dataType: "json",
		success: function (data) {
			console.log(data);
			alert(data['response']);
		}
		
	});
	
})