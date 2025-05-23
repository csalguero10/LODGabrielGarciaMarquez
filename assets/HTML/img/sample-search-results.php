<?php

/* obtain AJAX variables */
$search_key = (isset($_POST["s"])) ? strtolower($_POST["s"]) : "";
if ($search_key=="") exit;
$search_limit = (isset($_POST["l"])) ? $_POST["l"] : 10;

/* local sample data - should probably be a better idea to fetch these from a DB */
$demo_data = array(
	array( "type" => "page", "title" => "Welcome", "link" => "index.html" ),
	array( "type" => "page", "title" => "Home", "link" => "index.html" ),
	array( "type" => "page", "title" => "Blog", "link" => "blog.html" ),
	array( "type" => "page", "title" => "Journal", "link" => "blog.html" ),
	array( "type" => "page", "title" => "Features", "link" => "features.html" ),
	array( "type" => "page", "title" => "Shortcodes &amp; widgets", "link" => "features.html" ),
	array( "type" => "page", "title" => "Alert boxes", "link" => "features.html" ),
	array( "type" => "page", "title" => "Tab container", "link" => "features.html" ),
	array( "type" => "page", "title" => "Social icons", "link" => "features.html" ),
	array( "type" => "page", "title" => "Pricing tables", "link" => "features.html" ),
	array( "type" => "page", "title" => "Form elements", "link" => "features.html" ),
	array( "type" => "page", "title" => "Grid layout", "link" => "features.html" ),
	array( "type" => "page", "title" => "Typography", "link" => "features.html" ),
	array( "type" => "page", "title" => "Contact", "link" => "contact.html" ),
	array( "type" => "page", "title" => "Search results", "link" => "search.html" ),
	array( "type" => "page", "title" => "Sidebar template", "link" => "sidebar.html" ),
	array( "type" => "page", "title" => "Sidebar widgets", "link" => "sidebar.html" ),
	array( "type" => "page", "title" => "404 - Page not found", "link" => "404.html" ),
	array( "type" => "post", "title" => "Single post", "link" => "post.html" ),
	array( "type" => "category", "title" => "Chapter I: Less, but better", "link" => "blog.html" ),
	array( "type" => "category", "title" => "Chapter II: Practice safe design", "link" => "blog.html" ),
	array( "type" => "category", "title" => "Chapter III: As little design as possible", "link" => "blog.html" ),
	array( "type" => "category", "title" => "Chapter IV: Aesthetic, yet useful", "link" => "blog.html", "date" => "2015/07/07" ),
	array( "type" => "category", "title" => "Chapter V: Talking products", "link" => "blog.html" ),
);

function highlightkeyword($str, $search) {
	$occurrences = substr_count(strtolower($str), strtolower($search));
	$newstring = $str;
	$match = array();
	for ($i=0;$i<$occurrences;$i++) {
		$match[$i] = stripos($str, $search, $i);
		$match[$i] = substr($str, $match[$i], strlen($search));
		$newstring = str_replace($match[$i], '[[#]]' . $match[$i] . '[[@]]', strip_tags($newstring));
	}
	$newstring = str_replace('[[#]]', '<strong>', $newstring);
	$newstring = str_replace('[[@]]', '</strong>', $newstring);
	return $newstring;
}

$results_count = 0;
foreach ($demo_data as $demo_item) {

	// fuzzy search
	//if (strlen($search_key) - similar_text(strtolower($demo_item["title"]), $search_key) == 0) {

	// regular strpos search to speed things up a little
	if (stripos($demo_item["title"], $search_key) !== false) {
		echo '<li class="result"><a href="' . $demo_item["link"] .'">' . highlightkeyword($demo_item["title"], $search_key) . '</a></li>';
		$results_count++;
		if ($results_count >= $search_limit) {
			echo '<li class="result view-all"><a href="index.html">All results</a></li>';
			exit;
		}
	}
}
if ($results_count == 0) echo "<li><a>No results where found</a></li>";