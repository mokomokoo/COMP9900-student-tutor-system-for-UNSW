function box_key_pressing() {
	// set control + enter as pressed
	if ((event.keyCode === 10 || event.keyCode === 13) && event.ctrlKey) {
		send_input();
	}
	// set esc as pressed
	if (event.keyCode === 27) {
		input_box.blur();
	}
}


class chat_c {
	constructor() {
		this.msg_list = $('.msg-group');
	}
	
	//receive message
	receive_answer(name, msg) {
		this.msg_list.append(this.add_card(name, msg, 'left'));
		this.scroll(); 
	}
	
	//send message
	send_input(name, msg) {
		this.msg_list.append(this.add_card(name, msg, 'right'));
		this.scroll(); 
	}
	
	//message card
	add_card(name, msg, side) {
		var msg_temple = `
			<div class="card">
				 <div class="card-body">
					 <h6 class="card-subtitle mb-2 text-muted text-${side}">${name}</h6>
					 <p class="card-text float-${side}">${msg}</p>
				 </div>
			</div>
			`;
		return msg_temple;
	}

	scroll() {
		this.msg_list.scrollTop(this.msg_list[0].scrollHeight);
	}
}

var chat = new chat_c();
chat.receive_answer('Jarvis', 'You can ask me IT postgraduate course handbook information or concepts');
send_button = $('button') 
input_box = $('#input-box') 

//send input to the backend and get response
function send_input() {
	msg = input_box.val()
	if (msg != '') {
		chat.send_input('You', msg);
		$.ajax({
			url: "/chat",
			type: "POST",
			data: {
				'question':$("#input-box").val(),
			},
			dataType: "json",
			success: function (data) {
				console.log(data);
				chat.receive_answer('Jarvis', data['response']);
			}
			
		});
	}
}

send_button.on('click', send_input.bind());
input_box.on('keyup', box_key_pressing.bind());
