<?php

// Who you want to recieve the emails from the form. (Hint: generally you.)
$sendto = 'youremail@example.com';

// The subject you'll see in your inbox
$subject = 'Contact from contact form';

// Message for the user when he/she doesn't fill in the form correctly.
$errormessage = 'There seems to have been a problem. May we suggest:';

// Message for the user when he/she fills in the form correctly.
$thanks = "Thanks for the email! We'll get back to you as soon as possible!";

// Message for the bot when it fills in in at all.
$honeypot = "You filled in the honeypot! If you're human, try again!";

// Various messages displayed when the fields are empty.
$emptyname =  'Entering your name?';
$emptyemail = 'Entering your email address?';
$emptymessage = 'Entering a message?';

// Various messages displayed when the fields are incorrectly formatted.
$alertname =  'Entering your name using only the standard alphabet?';
$alertemail = 'Entering your email in this format: <em>name@example.com</em>?';

// Setting used variables.
$alert = '';
$pass = 0;

// Sanitizing the data, kind of done via error messages first. Twice is better!
function clean_var($variable) {
	$variable = strip_tags(stripslashes(trim(rtrim($variable))));
	return $variable;
}

// The first if for honeypot.
if ( empty($_REQUEST['last']) ) {

	// A bunch of if's for all the fields and the error messages.
	if ( empty($_REQUEST['name']) ) {
		$pass = 1;
		$alert .= "<li>" . $emptyname . "</li>";
	} elseif ( preg_match( "/[{}()*+?.\\^$|]/", $_REQUEST['name'] ) ) {
		$pass = 1;
		$alert .= "<li>" . $alertname . "</li>";
	}
	if ( empty($_REQUEST['email']) ) {
		$pass = 1;
		$alert .= "<li>" . $emptyemail . "</li>";
	} elseif ( ! filter_var( $_REQUEST['email'], FILTER_VALIDATE_EMAIL ) ) {
		$pass = 1;
		$alert .= "<li>" . $alertemail . "</li>";
	}
	if ( empty($_REQUEST['message']) ) {
		$pass = 1;
		$alert .= "<li>" . $emptymessage . "</li>";
	}

	// If the user err'd, print the error messages.
	if ( $pass==1 ) {

		//This first line is for ajax/javascript, comment it or delete it if this isn't your cup o' tea.
		echo "<script>$(\".message\").hide(0).show(\"200\");</script>";
		echo '<h4>' . $errormessage . '</h4>';
		echo '<ul class="small no-bottom">'.$alert.'</ul>';

	// If the user didn't err and there is in fact a message, time to email it.
	} elseif (isset($_REQUEST['message'])) {

		// Construct the message.
		$message = "From: " . clean_var($_REQUEST['name']) . "\n";
		$message .= "Email: " . clean_var($_REQUEST['email']) . "\n";
		$message .= "Message: \n" . clean_var($_REQUEST['message']);
		$header = 'From:'. clean_var($_REQUEST['email']);

		// Mail the message - for production
		mail($sendto, $subject, $message, $header);
		// This is for javascript, 
		echo "<script>$(\".message\").hide(0).show(\"200\").delay(6000).hide(0);$('#contact_form').clearForm();</script>";
		echo '<h4 class="no-bottom">' . $thanks . '</h4>';

		die();

		// Echo the email message - for development
		// echo "<br/><br/>" . $message;
	}
	
// If honeypot is filled, trigger the message that bot likely won't see.
} else {
	echo "<script>jQuery(\".message\").show(); </script>";
	echo $honeypot;
}
