/* enable CSS features that have JavaScript */
jQuery('html').removeClass('no-js');

/* determine if screen can handle touch events */
if ( ! (('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || (navigator.msMaxTouchPoints > 0))) {
	jQuery('html').addClass('no-touch');
}

/* simple way of determining if user is using a mouse */
var screenHasMouse = false;
function themeMouseMove() {
	screenHasMouse = true;
}
function themeTouchStart() {
	jQuery(window).off("mousemove");
	screenHasMouse = false;
	setTimeout(function() {
		jQuery(window).on("mousemove", themeMouseMove);
	}, 250);
}
if ( ! /(iPad|iPhone|iPod)/g.test(navigator.userAgent) ) {
	jQuery(window).on("touchstart", themeTouchStart).on("mousemove", themeMouseMove);
	if (window.navigator.msPointerEnabled) {
		document.addEventListener("MSPointerDown", themeTouchStart, false);
	}
}

jQuery(document).ready(function () { "use strict";

	/* toggle secondary panels visibility */
	jQuery('.secondary-links .links a').on('click', function(e) {
		var $this = jQuery(this), $thisClass = $this.attr('class').replace('toggle-','');
		jQuery('.secondary-links a').not($this).removeClass('on');
		$this.toggleClass('on');
		jQuery('.secondary').attr('class', function(index, classes) {
			return classes.replace(/(^|\s)open-\S+/g, '');
		});
		if (jQuery('.secondary-links a.on').length > 0) {
			jQuery('.secondary, .secondary-helper').addClass('open');
			jQuery('.secondary').addClass('open-' + $thisClass);
			jQuery('body').addClass('scrolling-disabled');
			jQuery('.go-to-top').removeClass('active');
		} else {
			jQuery('.secondary, .secondary-helper').removeClass('open');
			jQuery('body').removeClass('scrolling-disabled');
			jQuery(window).triggerHandler('scroll');
		}
		e.preventDefault();
	});

	/* clone the menu for mobile availability - avoid duplicating markup in the first place */
	jQuery('#panel-menu .mobile-menu').append(jQuery('#header #site-menu ul').first().clone());

	/* handle both mouse hover and touch events for traditional menu */
	jQuery(document).on({
		mouseenter: function () {
			if (screenHasMouse) {
				jQuery(this).addClass("hover");
			}
		},
		mouseleave: function () {
			if (screenHasMouse) {
				jQuery(this).removeClass("hover");
			}
		}
	}, '#site-menu li');
	if ( ! jQuery('html').hasClass('no-touch')) {
		jQuery('#site-menu li.menu-item-has-children > a').on('click', function (e) {
			if ( ! screenHasMouse && ! window.navigator.msPointerEnabled && ! jQuery('#site-menu').hasClass('mobile')) {
				var $parent = jQuery(this).parent();
				if ( ! $parent.parents('.hover').length) {
					jQuery('#site-menu li.menu-item-has-children').not($parent).removeClass('hover');
				}
				$parent.toggleClass("hover");
				e.preventDefault();
			}
		});

		/* toggle visibile dropdowns if touched outside the menu area */
		jQuery(document).on('click', function(e){
			if (jQuery(e.target).parents('#site-menu').length > 0) { return; }
			jQuery('#site-menu li.menu-item-has-children').removeClass('hover');
		});

		jQuery('.chapter-menu li.menu-item-has-children > a').on('click', function (e) {
			if (jQuery(this).parent().hasClass('current-menu-parent')) {
				return true;
			}
			e.preventDefault();
			jQuery('.chapter-menu li').removeClass('current-menu-parent').removeClass('current-menu-item');
			jQuery(this).parent().addClass('current-menu-parent');
		});

	}

	/* scroll to top functionality */
	var $back_to_top = jQuery('.go-to-top');
	if ($back_to_top.length > 0) {
		$back_to_top.on('click', function(e) {
			jQuery('html, body').animate({ scrollTop: 0 }, 600);
			e.preventDefault();
			return false;
		});
		jQuery(window).scroll(function() {
			$back_to_top.toggleClass("active", (jQuery(window).scrollTop() > jQuery('#header').height()));
		});
	}

	/* handle blockquote rotator pagination */
	jQuery('.blockquote-rotator').each(function() {
		var $blockquotes = jQuery('blockquote', this), pagination = jQuery('<div class="rotator-pagination"></div>'), iterator;
		$blockquotes.not(":eq(0)").hide();
		for (iterator = $blockquotes.length - 1; iterator >= 0; iterator--) {
			pagination.append('<span></span>');
		}
		jQuery('span:first-child', pagination).addClass('current');
		jQuery(this).append(pagination);
	});

	jQuery('.blockquote-rotator .rotator-pagination span').on('click', function(e) {
		var paginationParent = jQuery(this).parent(), currentIndex = paginationParent.find('.current').index(), clickedIndex = jQuery(this).index();
		if (currentIndex == clickedIndex) return;
		paginationParent.find('span:eq(' + currentIndex + ')').removeClass('current');
		paginationParent.find('span:eq(' + clickedIndex + ')').addClass('current');
		var rotator = paginationParent.parent();
		jQuery('blockquote:eq(' + currentIndex + ')', rotator).hide();
		jQuery('blockquote:eq(' + clickedIndex + ')', rotator).show();
	});

	/* handle skill progress bars initial animation */
	jQuery('.skill').each(function() {
		jQuery('.skill-level-active', this).animate({
			width: jQuery(this).data('value') + '%'
		}, {
			duration: 1000,
			step: function(now, fx) {
				jQuery(this).siblings('.skill-percentage').html(now.toFixed(0) + '%');
			}
		});
	});

	/* handle ajax search form */
	/* hide search form if ESC character is pressed */
	jQuery('.secondary #panel-search input[type=text]').keyup(function(e) {
		if (e.keyCode == 27) {
			jQuery('.secondary-links .toggle-search').triggerHandler('click');
		}
	});

	// check for keyboard events - add navigation within the results list
	jQuery('.secondary #panel-search input[type=text]').on('keypress keydown keyup', function(e){
		switch (e.keyCode) {
			case 13: // RETURN character
				e.preventDefault();
				if (jQuery('.secondary #panel-search .ajax-results .result').length > 0) {
					jQuery('.secondary-links .toggle-search').triggerHandler('click');
					window.location.href = jQuery('.secondary #panel-search .ajax-results .focus a').attr('href');
				}
				break;

			case 38: // up
				if (e.type == 'keydown') {
					var $focused = jQuery('.secondary #panel-search .ajax-results .focus'), $prev_focused = $focused.prev(':first');
					if ($prev_focused.length > 0) {
						$prev_focused.addClass('focus');
						$focused.removeClass('focus');
					}
				}
				e.preventDefault();
				break;

			case 40: // down
				if (e.type == 'keydown') {
					var $focused = jQuery('.secondary #panel-search .ajax-results .focus'), $next_focused = $focused.next(':first');
					if ($next_focused.length > 0) {
						$next_focused.addClass('focus');
						$focused.removeClass('focus');
					}
				}
				e.preventDefault();
				break;
		}
	});

	// trigger AJAX calls when input has changed
	jQuery('.secondary #panel-search .searchform.ajax input[type=text]').on("keyup", function(e) {
		clearTimeout(jQuery.data(this, 'timer'));
		var search_key = jQuery(this).val(); // obtain current search key
		if (search_key == '') {
			jQuery('.secondary #panel-search .ajax-results').fadeOut(); // hide results
		} else {
			if (search_key != jQuery(this).data("search_key") && search_key.length > 1) {
				// check if a non-character key is pressed
				jQuery(this).data("timer", setTimeout(ajax_search, 100)); // trigger the AJAX search
				jQuery(this).data("search_key", search_key);
			} else {
			}
		};
	});

	jQuery('.tabs a').on('click', function (e) {
		var $parent = jQuery(this).parent();
		e.preventDefault();
		if ($parent.hasClass('active')) return;
		$parent.siblings('li').each(function() {
			jQuery(this).removeClass('active');
			jQuery(jQuery(this).find('a').attr('href')).removeClass('active');
		});
		$parent.addClass('active');
		var hash = $parent.find('a').attr('href');
		jQuery(hash).addClass('active');
	});

});

function ajax_search() { "use strict";
	var search_key = jQuery('.secondary #panel-search .searchform.ajax input[type=text]').val();
	if(search_key !== '') {
		jQuery.ajax({
			type: "POST",
			url: jQuery('.secondary #panel-search .searchform.ajax').data('ajax-action'), // form must have a data-ajax-action attribute to point to the target URL
			data: {
				s: search_key, // search term
				l: 6 // limit for results list
			},
			cache: false,
			beforeSend: function() {
				jQuery('.secondary #panel-search .searchform').addClass('loading');
			},
			success: function(html) {
				jQuery('.secondary #panel-search .searchform').removeClass('loading');
				jQuery('.secondary #panel-search .ajax-results').html(html).fadeIn(); // load result into the list and fade the panel in
				jQuery('.secondary #panel-search .ajax-results li:first-child').addClass('focus');
			},
			error: function(jqXHR, textStatus, errorThrown) {
				if (jqXHR.statusText.indexOf('XMLHttpRequest') > -1) {
					jQuery('.secondary #panel-search .ajax-results').html('<li>Make sure you use an actual PHP based web server in order for this functionality to work properly.<li>').fadeIn();
				} else {
					jQuery('.secondary #panel-search .ajax-results').html('<li>' + jqXHR.statusText + '</li>').fadeIn();
				}
			}
		});
	}
	return false;
}