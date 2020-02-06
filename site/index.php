<html>
	<head>
		<link rel="stylesheet" type="text/css" href="index.css"></head>
		<title>Plant Monitor</title>

		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
		<script type="text/javascript">
			function sendData(){
				$(document).ready(function(){
					// JQuery ajax request please refer to reference 3.0
					$.ajax({url: "currentTime.php",type: "POST", data: {}, success: function(data){
						$('#time').html("Current Time: " + data);
					}});

					// JQuery ajax request please refer to reference 3.0
                                        $.ajax({url: "status.php",type: "POST", data: {}, success: function(data){
						if(data.includes("0")){
							$("#status").html("Water Status: Watered");
						}else{
							$("#status").html("Water Status: <span class='red'>Not Watered</div>");
						}
                                        }});
				});
			}

			setInterval(sendData,1000);
		</script>
	<body>
		<div id="wrapper">
			<p id="time" class="content">Current Time: NA</p>
			<p id="status" class="content">Water State: NA</p>
		</div>
	</body>
</html>
