<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg version="1.1" width="1200" height="395" onload="init(evt)" viewBox="0 0 1200 395" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<!-- Flame graph stack visualization. See https://github.com/brendangregg/FlameGraph for latest version, and http://www.brendangregg.com/flamegraphs.html for examples. -->
<!-- NOTES:  -->
<defs>
	<linearGradient id="background" y1="0" y2="1" x1="0" x2="0" >
		<stop stop-color="#eeeeee" offset="5%" />
		<stop stop-color="#eeeeb0" offset="95%" />
	</linearGradient>
</defs>
<style type="text/css">
	text { font-family:Verdana; font-size:13px; fill:rgb(0,0,0); }
	#search, #ignorecase { opacity:0.1; cursor:pointer; }
	#search:hover, #search.show, #ignorecase:hover, #ignorecase.show { opacity:1; }
	#subtitle { text-anchor:middle; font-color:rgb(160,160,160); }
	#title { text-anchor:middle; font-size:18px}
	#unzoom { cursor:pointer; }
	#frames > *:hover { stroke:black; stroke-width:0.5; cursor:pointer; }
	.hide { display:none; }
	.parent { opacity:0.5; }
</style>
<script type="text/ecmascript">
<![CDATA[
	"use strict";
	var details, searchbtn, unzoombtn, matchedtxt, svg, searching, currentSearchTerm, ignorecase, ignorecaseBtn;
	function init(evt) {
		details = document.getElementById("details").firstChild;
		searchbtn = document.getElementById("search");
		ignorecaseBtn = document.getElementById("ignorecase");
		unzoombtn = document.getElementById("unzoom");
		matchedtxt = document.getElementById("matched");
		svg = document.getElementsByTagName("svg")[0];
		searching = 0;
		currentSearchTerm = null;

		// use GET parameters to restore a flamegraphs state.
		var params = get_params();
		if (params.x && params.y)
			zoom(find_group(document.querySelector('[x="' + params.x + '"][y="' + params.y + '"]')));
                if (params.s) search(params.s);
	}

	// event listeners
	window.addEventListener("click", function(e) {
		var target = find_group(e.target);
		if (target) {
			if (target.nodeName == "a") {
				if (e.ctrlKey === false) return;
				e.preventDefault();
			}
			if (target.classList.contains("parent")) unzoom();
			zoom(target);
			if (!document.querySelector('.parent')) {
				clearzoom();
				return;
			}

			// set parameters for zoom state
			var el = target.querySelector("rect");
			if (el && el.attributes && el.attributes.y && el.attributes._orig_x) {
				var params = get_params()
				params.x = el.attributes._orig_x.value;
				params.y = el.attributes.y.value;
				history.replaceState(null, null, parse_params(params));
			}
		}
		else if (e.target.id == "unzoom") clearzoom();
		else if (e.target.id == "search") search_prompt();
		else if (e.target.id == "ignorecase") toggle_ignorecase();
	}, false)

	// mouse-over for info
	// show
	window.addEventListener("mouseover", function(e) {
		var target = find_group(e.target);
		if (target) details.nodeValue = "Function: " + g_to_text(target);
	}, false)

	// clear
	window.addEventListener("mouseout", function(e) {
		var target = find_group(e.target);
		if (target) details.nodeValue = ' ';
	}, false)

	// ctrl-F for search
	// ctrl-I to toggle case-sensitive search
	window.addEventListener("keydown",function (e) {
		if (e.keyCode === 114 || (e.ctrlKey && e.keyCode === 70)) {
			e.preventDefault();
			search_prompt();
		}
		else if (e.ctrlKey && e.keyCode === 73) {
			e.preventDefault();
			toggle_ignorecase();
		}
	}, false)

	// functions
	function get_params() {
		var params = {};
		var paramsarr = window.location.search.substr(1).split('&');
		for (var i = 0; i < paramsarr.length; ++i) {
			var tmp = paramsarr[i].split("=");
			if (!tmp[0] || !tmp[1]) continue;
			params[tmp[0]]  = decodeURIComponent(tmp[1]);
		}
		return params;
	}
	function parse_params(params) {
		var uri = "?";
		for (var key in params) {
			uri += key + '=' + encodeURIComponent(params[key]) + '&';
		}
		if (uri.slice(-1) == "&")
			uri = uri.substring(0, uri.length - 1);
		if (uri == '?')
			uri = window.location.href.split('?')[0];
		return uri;
	}
	function find_child(node, selector) {
		var children = node.querySelectorAll(selector);
		if (children.length) return children[0];
	}
	function find_group(node) {
		var parent = node.parentElement;
		if (!parent) return;
		if (parent.id == "frames") return node;
		return find_group(parent);
	}
	function orig_save(e, attr, val) {
		if (e.attributes["_orig_" + attr] != undefined) return;
		if (e.attributes[attr] == undefined) return;
		if (val == undefined) val = e.attributes[attr].value;
		e.setAttribute("_orig_" + attr, val);
	}
	function orig_load(e, attr) {
		if (e.attributes["_orig_"+attr] == undefined) return;
		e.attributes[attr].value = e.attributes["_orig_" + attr].value;
		e.removeAttribute("_orig_"+attr);
	}
	function g_to_text(e) {
		var text = find_child(e, "title").firstChild.nodeValue;
		return (text)
	}
	function g_to_func(e) {
		var func = g_to_text(e);
		// if there's any manipulation we want to do to the function
		// name before it's searched, do it here before returning.
		return (func);
	}
	function update_text(e) {
		var r = find_child(e, "rect");
		var t = find_child(e, "text");
		var w = parseFloat(r.attributes.width.value) -3;
		var txt = find_child(e, "title").textContent.replace(/\([^(]*\)$/,"");
		t.attributes.x.value = parseFloat(r.attributes.x.value) + 3;

		// Smaller than this size won't fit anything
		if (w < 2 * 13 * 0.59) {
			t.textContent = "";
			return;
		}

		t.textContent = txt;
		// Fit in full text width
		if (/^ *$/.test(txt) || t.getSubStringLength(0, txt.length) < w)
			return;

		for (var x = txt.length - 2; x > 0; x--) {
			if (t.getSubStringLength(0, x + 2) <= w) {
				t.textContent = txt.substring(0, x) + "..";
				return;
			}
		}
		t.textContent = "";
	}

	// zoom
	function zoom_reset(e) {
		if (e.attributes != undefined) {
			orig_load(e, "x");
			orig_load(e, "width");
		}
		if (e.childNodes == undefined) return;
		for (var i = 0, c = e.childNodes; i < c.length; i++) {
			zoom_reset(c[i]);
		}
	}
	function zoom_child(e, x, ratio) {
		if (e.attributes != undefined) {
			if (e.attributes.x != undefined) {
				orig_save(e, "x");
				e.attributes.x.value = (parseFloat(e.attributes.x.value) - x - 10) * ratio + 10;
				if (e.tagName == "text")
					e.attributes.x.value = find_child(e.parentNode, "rect[x]").attributes.x.value + 3;
			}
			if (e.attributes.width != undefined) {
				orig_save(e, "width");
				e.attributes.width.value = parseFloat(e.attributes.width.value) * ratio;
			}
		}

		if (e.childNodes == undefined) return;
		for (var i = 0, c = e.childNodes; i < c.length; i++) {
			zoom_child(c[i], x - 10, ratio);
		}
	}
	function zoom_parent(e) {
		if (e.attributes) {
			if (e.attributes.x != undefined) {
				orig_save(e, "x");
				e.attributes.x.value = 10;
			}
			if (e.attributes.width != undefined) {
				orig_save(e, "width");
				e.attributes.width.value = parseInt(svg.width.baseVal.value) - (10 * 2);
			}
		}
		if (e.childNodes == undefined) return;
		for (var i = 0, c = e.childNodes; i < c.length; i++) {
			zoom_parent(c[i]);
		}
	}
	function zoom(node) {
		var attr = find_child(node, "rect").attributes;
		var width = parseFloat(attr.width.value);
		var xmin = parseFloat(attr.x.value);
		var xmax = parseFloat(xmin + width);
		var ymin = parseFloat(attr.y.value);
		var ratio = (svg.width.baseVal.value - 2 * 10) / width;

		// XXX: Workaround for JavaScript float issues (fix me)
		var fudge = 0.0001;

		unzoombtn.classList.remove("hide");

		var el = document.getElementById("frames").children;
		for (var i = 0; i < el.length; i++) {
			var e = el[i];
			var a = find_child(e, "rect").attributes;
			var ex = parseFloat(a.x.value);
			var ew = parseFloat(a.width.value);
			var upstack;
			// Is it an ancestor
			if (1 == 0) {
				upstack = parseFloat(a.y.value) > ymin;
			} else {
				upstack = parseFloat(a.y.value) < ymin;
			}
			if (upstack) {
				// Direct ancestor
				if (ex <= xmin && (ex+ew+fudge) >= xmax) {
					e.classList.add("parent");
					zoom_parent(e);
					update_text(e);
				}
				// not in current path
				else
					e.classList.add("hide");
			}
			// Children maybe
			else {
				// no common path
				if (ex < xmin || ex + fudge >= xmax) {
					e.classList.add("hide");
				}
				else {
					zoom_child(e, xmin, ratio);
					update_text(e);
				}
			}
		}
		search();
	}
	function unzoom() {
		unzoombtn.classList.add("hide");
		var el = document.getElementById("frames").children;
		for(var i = 0; i < el.length; i++) {
			el[i].classList.remove("parent");
			el[i].classList.remove("hide");
			zoom_reset(el[i]);
			update_text(el[i]);
		}
		search();
	}
	function clearzoom() {
		unzoom();

		// remove zoom state
		var params = get_params();
		if (params.x) delete params.x;
		if (params.y) delete params.y;
		history.replaceState(null, null, parse_params(params));
	}

	// search
	function toggle_ignorecase() {
		ignorecase = !ignorecase;
		if (ignorecase) {
			ignorecaseBtn.classList.add("show");
		} else {
			ignorecaseBtn.classList.remove("show");
		}
		reset_search();
		search();
	}
	function reset_search() {
		var el = document.querySelectorAll("#frames rect");
		for (var i = 0; i < el.length; i++) {
			orig_load(el[i], "fill")
		}
		var params = get_params();
		delete params.s;
		history.replaceState(null, null, parse_params(params));
	}
	function search_prompt() {
		if (!searching) {
			var term = prompt("Enter a search term (regexp " +
			    "allowed, eg: ^ext4_)"
			    + (ignorecase ? ", ignoring case" : "")
			    + "\nPress Ctrl-i to toggle case sensitivity", "");
			if (term != null) search(term);
		} else {
			reset_search();
			searching = 0;
			currentSearchTerm = null;
			searchbtn.classList.remove("show");
			searchbtn.firstChild.nodeValue = "Search"
			matchedtxt.classList.add("hide");
			matchedtxt.firstChild.nodeValue = ""
		}
	}
	function search(term) {
		if (term) currentSearchTerm = term;

		var re = new RegExp(currentSearchTerm, ignorecase ? 'i' : '');
		var el = document.getElementById("frames").children;
		var matches = new Object();
		var maxwidth = 0;
		for (var i = 0; i < el.length; i++) {
			var e = el[i];
			var func = g_to_func(e);
			var rect = find_child(e, "rect");
			if (func == null || rect == null)
				continue;

			// Save max width. Only works as we have a root frame
			var w = parseFloat(rect.attributes.width.value);
			if (w > maxwidth)
				maxwidth = w;

			if (func.match(re)) {
				// highlight
				var x = parseFloat(rect.attributes.x.value);
				orig_save(rect, "fill");
				rect.attributes.fill.value = "rgb(230,0,230)";

				// remember matches
				if (matches[x] == undefined) {
					matches[x] = w;
				} else {
					if (w > matches[x]) {
						// overwrite with parent
						matches[x] = w;
					}
				}
				searching = 1;
			}
		}
		if (!searching)
			return;
		var params = get_params();
		params.s = currentSearchTerm;
		history.replaceState(null, null, parse_params(params));

		searchbtn.classList.add("show");
		searchbtn.firstChild.nodeValue = "Reset Search";

		// calculate percent matched, excluding vertical overlap
		var count = 0;
		var lastx = -1;
		var lastw = 0;
		var keys = Array();
		for (k in matches) {
			if (matches.hasOwnProperty(k))
				keys.push(k);
		}
		// sort the matched frames by their x location
		// ascending, then width descending
		keys.sort(function(a, b){
			return a - b;
		});
		// Step through frames saving only the biggest bottom-up frames
		// thanks to the sort order. This relies on the tree property
		// where children are always smaller than their parents.
		var fudge = 0.0001;	// JavaScript floating point
		for (var k in keys) {
			var x = parseFloat(keys[k]);
			var w = matches[keys[k]];
			if (x >= lastx + lastw - fudge) {
				count += w;
				lastx = x;
				lastw = w;
			}
		}
		// display matched percent
		matchedtxt.classList.remove("hide");
		var pct = 100 * count / maxwidth;
		if (pct != 100) pct = pct.toFixed(1)
		matchedtxt.firstChild.nodeValue = "Matched: " + pct + "%";
	}
]]>
</script>
<rect x="0.0" y="0" width="1200.0" height="395.0" fill="url(#background)"  />
<text id="title" x="600.00" y="26" >Firedrake example</text>
<text id="details" x="10.00" y="377" > </text>
<text id="unzoom" x="10.00" y="26" class="hide">Reset Zoom</text>
<text id="search" x="1090.00" y="26" >Search</text>
<text id="ignorecase" x="1174.00" y="26" >ic</text>
<text id="matched" x="1090.00" y="377" > </text>
<g id="frames">
<g >
<title>pyop2.parloop.JITModule.compile (1,329,479 us, 0.10%)</title><rect x="1138.3" y="199" width="1.1" height="15.0" fill="rgb(150.333834569036,150.333834569036,120.84858291148)" rx="2" ry="2" />
<text  x="1141.26" y="209.5" ></text>
</g>
<g >
<title>pyop2.parloop.JITModule.compile (10,593,033 us, 0.77%)</title><rect x="777.4" y="231" width="9.1" height="15.0" fill="rgb(121.102371965975,121.102371965975,150.858523606318)" rx="2" ry="2" />
<text  x="780.37" y="241.5" ></text>
</g>
<g >
<title>firedrake.tsfc_interface.compile_form (1,029,946 us, 0.07%)</title><rect x="1189.1" y="167" width="0.9" height="15.0" fill="rgb(112.13504389799,146.109085455034,146.109085455034)" rx="2" ry="2" />
<text  x="1192.12" y="177.5" ></text>
</g>
<g >
<title>pyop2.parloop.JITModule.compile (15,366,386 us, 1.12%)</title><rect x="205.0" y="151" width="13.2" height="15.0" fill="rgb(148.639797437274,159.52375390556,148.639797437274)" rx="2" ry="2" />
<text  x="207.99" y="161.5" ></text>
</g>
<g >
<title>firedrake.assemble_expressions.evaluate_expression (3,873,835 us, 0.28%)</title><rect x="131.6" y="103" width="3.3" height="15.0" fill="rgb(148.601630726533,148.601630726533,112.454056597813)" rx="2" ry="2" />
<text  x="134.60" y="113.5" ></text>
</g>
<g >
<title>ParLoop_Cells_wrap_wrap_slate_loopy_knl_3 (3,146,213 us, 0.23%)</title><rect x="992.4" y="311" width="2.7" height="15.0" fill="rgb(152.191722610125,152.191722610125,129.852194187526)" rx="2" ry="2" />
<text  x="995.39" y="321.5" ></text>
</g>
<g >
<title>MatMultTranspose (4,297,805 us, 0.31%)</title><rect x="1127.7" y="231" width="3.7" height="15.0" fill="rgb(145.739115503133,159.99595794135,145.739115503133)" rx="2" ry="2" />
<text  x="1130.75" y="241.5" ></text>
</g>
<g >
<title>firedrake.assemble.assemble_form (32,688,059 us, 2.38%)</title><rect x="802.3" y="183" width="28.1" height="15.0" fill="rgb(138.031424501821,106.830525285917,138.031424501821)" rx="2" ry="2" />
<text  x="805.34" y="193.5" >f..</text>
</g>
<g >
<title>pyop2.parloop.JITModule.compile (1,037,558 us, 0.08%)</title><rect x="727.7" y="215" width="0.9" height="15.0" fill="rgb(142.204011312972,117.522778989491,142.204011312972)" rx="2" ry="2" />
<text  x="730.73" y="225.5" ></text>
</g>
<g >
<title>ParLoopExecute (20,987,988 us, 1.53%)</title><rect x="882.2" y="215" width="18.0" height="15.0" fill="rgb(117.442253415136,117.442253415136,150.15011356422)" rx="2" ry="2" />
<text  x="885.18" y="225.5" ></text>
</g>
<g >
<title>pyop2.parloop.JITModule.compile (8,603,413 us, 0.63%)</title><rect x="322.5" y="167" width="7.4" height="15.0" fill="rgb(156.419586962442,145.883500045387,145.883500045387)" rx="2" ry="2" />
<text  x="325.51" y="177.5" ></text>
</g>
<g >
<title>firedrake.assemble.assemble_form (1,461,976 us, 0.11%)</title><rect x="950.3" y="231" width="1.2" height="15.0" fill="rgb(117.775445245355,147.571411730277,147.571411730277)" rx="2" ry="2" />
<text  x="953.26" y="241.5" ></text>
</g>
<g >
<title>firedrake.assemble.assemble (39,866,339 us, 2.90%)</title><rect x="339.3" y="119" width="34.2" height="15.0" fill="rgb(151.75030125225,151.75030125225,127.712998376288)" rx="2" ry="2" />
<text  x="342.27" y="129.5" >fi..</text>
</g>
<g >
<title>KSPSetUp (105,300,943 us, 7.67%)</title><rect x="1019.6" y="215" width="90.4" height="15.0" fill="rgb(139.935605556655,111.709989238928,139.935605556655)" rx="2" ry="2" />
<text  x="1022.57" y="225.5" >KSPSetUp</text>
</g>
<g >
<title>PCSetUp (29,804,738 us, 2.17%)</title><rect x="1131.4" y="167" width="25.6" height="15.0" fill="rgb(117.303176557254,147.448971700029,147.448971700029)" rx="2" ry="2" />
<text  x="1134.44" y="177.5" >P..</text>
</g>
<g >
<title>ParLoopExecute (1,969,052 us, 0.14%)</title><rect x="1159.7" y="167" width="1.7" height="15.0" fill="rgb(150.636415376562,150.636415376562,122.314936055644)" rx="2" ry="2" />
<text  x="1162.71" y="177.5" ></text>
</g>
<g >
<title>firedrake.pointquery_utils.to_reference_coordinates (327,971 us, 0.02%)</title><rect x="1000.9" y="295" width="0.2" height="15.0" fill="rgb(133.740144271059,95.8341196945893,133.740144271059)" rx="2" ry="2" />
<text  x="1003.85" y="305.5" ></text>
</g>
<g >
<title>ParLoopExecute (2,660,361 us, 0.19%)</title><rect x="1137.1" y="183" width="2.3" height="15.0" fill="rgb(135.048166878878,152.049524746376,152.049524746376)" rx="2" ry="2" />
<text  x="1140.12" y="193.5" ></text>
</g>
<g >
<title>ParLoopExecute (1,497,436 us, 0.11%)</title><rect x="1122.1" y="295" width="1.3" height="15.0" fill="rgb(136.765960487062,152.494878644794,152.494878644794)" rx="2" ry="2" />
<text  x="1125.09" y="305.5" ></text>
</g>
<g >
<title>firedrake.dmhooks.coarsen (14,271,030 us, 1.04%)</title><rect x="1115.5" y="247" width="12.2" height="15.0" fill="rgb(148.207796420723,159.59407965244,148.207796420723)" rx="2" ry="2" />
<text  x="1118.49" y="257.5" ></text>
</g>
<g >
<title>ParLoopExecute (21,598,878 us, 1.57%)</title><rect x="767.9" y="215" width="18.6" height="15.0" fill="rgb(147.789509452493,147.789509452493,108.518391962081)" rx="2" ry="2" />
<text  x="770.91" y="225.5" ></text>
</g>
<g >
<title>firedrake.mg.interface.inject (9,142,418 us, 0.67%)</title><rect x="1119.9" y="279" width="7.8" height="15.0" fill="rgb(106.065384021178,144.535469931417,144.535469931417)" rx="2" ry="2" />
<text  x="1122.89" y="289.5" ></text>
</g>
<g >
<title>firedrake.assemble.assemble (43,919,773 us, 3.20%)</title><rect x="792.7" y="167" width="37.7" height="15.0" fill="rgb(156.437214867535,146.018647317772,146.018647317772)" rx="2" ry="2" />
<text  x="795.69" y="177.5" >fi..</text>
</g>
<g >
<title>firedrake.assemble.assemble_form (19,554,980 us, 1.42%)</title><rect x="1173.2" y="151" width="16.8" height="15.0" fill="rgb(154.229427099516,154.229427099516,139.727223636116)" rx="2" ry="2" />
<text  x="1176.20" y="161.5" ></text>
</g>
<g >
<title>CreateExtMesh (7,179,910 us, 0.52%)</title><rect x="121.1" y="71" width="6.2" height="15.0" fill="rgb(127.805360132561,162.915406490048,127.805360132561)" rx="2" ry="2" />
<text  x="124.13" y="81.5" ></text>
</g>
<g >
<title>ParLoopExecute (1,250,805 us, 0.09%)</title><rect x="1003.8" y="295" width="1.1" height="15.0" fill="rgb(143.953831787458,154.358400833785,154.358400833785)" rx="2" ry="2" />
<text  x="1006.84" y="305.5" ></text>
</g>
<g >
<title>KSPSolve (30,457,388 us, 2.22%)</title><rect x="975.0" y="215" width="26.1" height="15.0" fill="rgb(128.429821857065,128.429821857065,152.276739714271)" rx="2" ry="2" />
<text  x="977.98" y="225.5" >K..</text>
</g>
<g >
<title>firedrake.__init__ (2,406,134 us, 0.18%)</title><rect x="127.3" y="71" width="2.1" height="15.0" fill="rgb(153.14948392021,153.14948392021,134.493652844097)" rx="2" ry="2" />
<text  x="130.29" y="81.5" ></text>
</g>
<g >
<title>firedrake.assemble.allocate_matrix (122,832 us, 0.01%)</title><rect x="256.4" y="87" width="0.1" height="15.0" fill="rgb(149.02150481974,149.02150481974,114.488831049508)" rx="2" ry="2" />
<text  x="259.41" y="97.5" ></text>
</g>
<g >
<title>firedrake.variational_solver.NonlinearVariationalSolver.solve (870,830,179 us, 63.41%)</title><rect x="441.8" y="87" width="748.2" height="15.0" fill="rgb(153.519786923181,123.651699744389,123.651699744389)" rx="2" ry="2" />
<text  x="444.81" y="97.5" >firedrake.variational_solver.NonlinearVariationalSolver.solve</text>
</g>
<g >
<title>HybridInit (4,027,528 us, 0.29%)</title><rect x="1157.9" y="135" width="3.5" height="15.0" fill="rgb(145.811053176845,126.765823765665,145.811053176845)" rx="2" ry="2" />
<text  x="1160.95" y="145.5" ></text>
</g>
<g >
<title>SCBackSub (150,175,941 us, 10.93%)</title><rect x="701.4" y="151" width="129.0" height="15.0" fill="rgb(138.691690061161,138.691690061161,154.262907753773)" rx="2" ry="2" />
<text  x="704.40" y="161.5" >SCBackSub</text>
</g>
<g >
<title>KSPSolve (91,998,465 us, 6.70%)</title><rect x="1031.0" y="231" width="79.0" height="15.0" fill="rgb(135.149124019309,99.4446302994784,135.149124019309)" rx="2" ry="2" />
<text  x="1034.00" y="241.5" >KSPSolve</text>
</g>
<g >
<title>firedrake.tsfc_interface.compile_form (1,014,374 us, 0.07%)</title><rect x="255.4" y="135" width="0.9" height="15.0" fill="rgb(106.114472874902,144.548196671271,144.548196671271)" rx="2" ry="2" />
<text  x="258.42" y="145.5" ></text>
</g>
<g >
<title>firedrake.tsfc_interface.compile_form (380,217 us, 0.03%)</title><rect x="1156.7" y="215" width="0.3" height="15.0" fill="rgb(130.226640672371,150.799499433578,150.799499433578)" rx="2" ry="2" />
<text  x="1159.69" y="225.5" ></text>
</g>
<g >
<title>firedrake.mg.embedded.TransferManager.op (11,698,763 us, 0.85%)</title><rect x="1117.7" y="263" width="10.0" height="15.0" fill="rgb(135.628487740466,100.672999834945,135.628487740466)" rx="2" ry="2" />
<text  x="1120.70" y="273.5" ></text>
</g>
<g >
<title>ParLoopExecute (9,677,907 us, 0.70%)</title><rect x="1148.4" y="215" width="8.3" height="15.0" fill="rgb(156.347912936705,145.333999181406,145.333999181406)" rx="2" ry="2" />
<text  x="1151.38" y="225.5" ></text>
</g>
<g >
<title>firedrake.slate.slac.compiler.compile_expression (7,240,906 us, 0.53%)</title><rect x="786.5" y="215" width="6.2" height="15.0" fill="rgb(146.826298532841,159.818974657444,146.826298532841)" rx="2" ry="2" />
<text  x="789.47" y="225.5" ></text>
</g>
<g >
<title>PCSetUp (147,266,335 us, 10.72%)</title><rect x="1004.9" y="199" width="126.5" height="15.0" fill="rgb(138.685494698222,108.506580164193,138.685494698222)" rx="2" ry="2" />
<text  x="1007.91" y="209.5" >PCSetUp</text>
</g>
<g >
<title>firedrake.interpolation.interpolate (4,783,853 us, 0.35%)</title><rect x="1123.4" y="295" width="4.1" height="15.0" fill="rgb(114.184442198395,146.640410940325,146.640410940325)" rx="2" ry="2" />
<text  x="1126.38" y="305.5" ></text>
</g>
<g >
<title>firedrake.interpolation.Interpolator.interpolate (3,497,627 us, 0.25%)</title><rect x="1124.4" y="311" width="3.0" height="15.0" fill="rgb(138.963024354165,109.217749907547,138.963024354165)" rx="2" ry="2" />
<text  x="1127.43" y="321.5" ></text>
</g>
<g >
<title>MatLUFactorNum (132,911 us, 0.01%)</title><rect x="290.6" y="119" width="0.2" height="15.0" fill="rgb(110.145364280143,145.593242591148,145.593242591148)" rx="2" ry="2" />
<text  x="293.64" y="129.5" ></text>
</g>
<g >
<title>ParLoop_Cells_wrap_wrap_slate_loopy_knl_3 (625,049 us, 0.05%)</title><rect x="1004.4" y="311" width="0.5" height="15.0" fill="rgb(156.58565438002,147.156683580152,147.156683580152)" rx="2" ry="2" />
<text  x="1007.38" y="321.5" ></text>
</g>
<g >
<title>firedrake.assemble.assemble_form (9,448,713 us, 0.69%)</title><rect x="987.0" y="279" width="8.1" height="15.0" fill="rgb(152.639583340186,116.903472274759,116.903472274759)" rx="2" ry="2" />
<text  x="989.97" y="289.5" ></text>
</g>
<g >
<title>firedrake.assemble.assemble (52,094,076 us, 3.79%)</title><rect x="1065.3" y="279" width="44.7" height="15.0" fill="rgb(144.301901225537,160.229923056308,144.301901225537)" rx="2" ry="2" />
<text  x="1068.29" y="289.5" >fir..</text>
</g>
<g >
<title>HybridRHS (66,717,323 us, 4.86%)</title><rect x="847.0" y="167" width="57.4" height="15.0" fill="rgb(152.263464202549,152.263464202549,130.199864981581)" rx="2" ry="2" />
<text  x="850.04" y="177.5" >Hybri..</text>
</g>
<g >
<title>ParLoopExecute (2,552,166 us, 0.19%)</title><rect x="132.7" y="119" width="2.2" height="15.0" fill="rgb(123.07206207964,148.944608687314,148.944608687314)" rx="2" ry="2" />
<text  x="135.72" y="129.5" ></text>
</g>
<g >
<title>perfsolve (950,319,885 us, 69.19%)</title><rect x="373.5" y="71" width="816.5" height="15.0" fill="rgb(119.953221018135,119.953221018135,150.636107293833)" rx="2" ry="2" />
<text  x="376.52" y="81.5" >perfsolve</text>
</g>
<g >
<title>firedrake.extrusion_utils.make_extruded_coords (5,287,504 us, 0.38%)</title><rect x="122.7" y="87" width="4.5" height="15.0" fill="rgb(149.111439121937,149.111439121937,114.924666514001)" rx="2" ry="2" />
<text  x="125.69" y="97.5" ></text>
</g>
<g >
<title>firedrake.tsfc_interface.compile_form (840,187 us, 0.06%)</title><rect x="218.6" y="135" width="0.7" height="15.0" fill="rgb(132.402374644793,162.167055290383,132.402374644793)" rx="2" ry="2" />
<text  x="221.58" y="145.5" ></text>
</g>
<g >
<title>ParLoopExecute (2,331,342 us, 0.17%)</title><rect x="1125.4" y="327" width="2.0" height="15.0" fill="rgb(150.011313385153,150.011313385153,119.285595635739)" rx="2" ry="2" />
<text  x="1128.43" y="337.5" ></text>
</g>
<g >
<title>firedrake.matrix_free.operators.ImplicitMatrixContext.mult (15,762,472 us, 1.15%)</title><rect x="981.5" y="247" width="13.6" height="15.0" fill="rgb(124.697932676162,149.36613069382,149.36613069382)" rx="2" ry="2" />
<text  x="984.55" y="257.5" ></text>
</g>
<g >
<title>pyop2.parloop.JITModule.compile (1,165,192 us, 0.08%)</title><rect x="1126.4" y="343" width="1.0" height="15.0" fill="rgb(155.042479374467,135.325675204244,135.325675204244)" rx="2" ry="2" />
<text  x="1129.43" y="353.5" ></text>
</g>
<g >
<title>firedrake.assemble.assemble_form (15,282,268 us, 1.11%)</title><rect x="1143.9" y="199" width="13.1" height="15.0" fill="rgb(153.716593889592,125.160553153537,125.160553153537)" rx="2" ry="2" />
<text  x="1146.89" y="209.5" ></text>
</g>
<g >
<title>firedrake.slate.slac.compiler.compile_expression (4,291,975 us, 0.31%)</title><rect x="1106.4" y="311" width="3.6" height="15.0" fill="rgb(130.748380633233,130.748380633233,152.725493025787)" rx="2" ry="2" />
<text  x="1109.36" y="321.5" ></text>
</g>
<g >
<title>MatMult (18,922,719 us, 1.38%)</title><rect x="978.8" y="231" width="16.3" height="15.0" fill="rgb(152.598535376202,144.158746901517,152.598535376202)" rx="2" ry="2" />
<text  x="981.83" y="241.5" ></text>
</g>
<g >
<title>ParLoopExecute (2,076,322 us, 0.15%)</title><rect x="726.8" y="199" width="1.8" height="15.0" fill="rgb(140.427874184303,140.427874184303,154.59894339051)" rx="2" ry="2" />
<text  x="729.84" y="209.5" ></text>
</g>
<g >
<title>HybridBreak (4,564,804 us, 0.33%)</title><rect x="843.1" y="167" width="3.9" height="15.0" fill="rgb(130.848431322755,130.848431322755,152.744857675372)" rx="2" ry="2" />
<text  x="846.12" y="177.5" ></text>
</g>
<g >
<title>firedrake.tsfc_interface.compile_form (1,601,209 us, 0.12%)</title><rect x="1108.7" y="327" width="1.3" height="15.0" fill="rgb(154.155254979674,154.155254979674,139.367774132266)" rx="2" ry="2" />
<text  x="1111.67" y="337.5" ></text>
</g>
<g >
<title>firedrake.assemble.assemble_form (44,081,201 us, 3.21%)</title><rect x="754.8" y="199" width="37.9" height="15.0" fill="rgb(106.977669285146,144.771988333186,144.771988333186)" rx="2" ry="2" />
<text  x="757.82" y="209.5" >fi..</text>
</g>
<g >
<title>firedrake.mg.embedded.TransferManager.op (4,395,330 us, 0.32%)</title><rect x="997.4" y="263" width="3.7" height="15.0" fill="rgb(124.802605945017,124.802605945017,151.574697924842)" rx="2" ry="2" />
<text  x="1000.36" y="273.5" ></text>
</g>
<g >
<title>ParLoopExecute (12,650,615 us, 0.92%)</title><rect x="244.6" y="135" width="10.8" height="15.0" fill="rgb(136.456891478125,136.456891478125,153.83036609254)" rx="2" ry="2" />
<text  x="247.56" y="145.5" ></text>
</g>
<g >
<title>pyop2.parloop.JITModule.compile (1,742,947 us, 0.13%)</title><rect x="125.7" y="119" width="1.5" height="15.0" fill="rgb(149.239462189837,149.239462189837,115.545085996903)" rx="2" ry="2" />
<text  x="128.73" y="129.5" ></text>
</g>
<g >
<title>pyop2.parloop.JITModule.compile (748,324 us, 0.05%)</title><rect x="1122.7" y="311" width="0.7" height="15.0" fill="rgb(115.982408608886,147.106550380082,147.106550380082)" rx="2" ry="2" />
<text  x="1125.73" y="321.5" ></text>
</g>
<g >
<title>ParLoop_Cells_wrap_wrap_slate_loopy_knl_3 (486,080 us, 0.04%)</title><rect x="951.1" y="263" width="0.4" height="15.0" fill="rgb(143.338642288419,160.386732650722,143.338642288419)" rx="2" ry="2" />
<text  x="954.10" y="273.5" ></text>
</g>
<g >
<title>firedrake.mg.interface.restrict (3,125,649 us, 0.23%)</title><rect x="1128.8" y="247" width="2.6" height="15.0" fill="rgb(136.175950246231,161.552752285497,136.175950246231)" rx="2" ry="2" />
<text  x="1131.75" y="257.5" ></text>
</g>
<g >
<title>firedrake.assemble.assemble (53,085,257 us, 3.87%)</title><rect x="858.8" y="183" width="45.6" height="15.0" fill="rgb(120.703033544929,148.330416104241,148.330416104241)" rx="2" ry="2" />
<text  x="861.75" y="193.5" >fir..</text>
</g>
<g >
<title>SNESFunctionEval (33,281,045 us, 2.42%)</title><rect x="1161.4" y="119" width="28.6" height="15.0" fill="rgb(126.861297213674,163.069091151262,126.861297213674)" rx="2" ry="2" />
<text  x="1164.41" y="129.5" >S..</text>
</g>
<g >
<title>firedrake.assemble.assemble (28,358,040 us, 2.06%)</title><rect x="231.9" y="103" width="24.4" height="15.0" fill="rgb(137.736454003601,152.746488075008,152.746488075008)" rx="2" ry="2" />
<text  x="234.93" y="113.5" >f..</text>
</g>
<g >
<title>ParLoopExecute (1,570,811 us, 0.11%)</title><rect x="1129.8" y="263" width="1.3" height="15.0" fill="rgb(153.625956004922,124.465662704403,124.465662704403)" rx="2" ry="2" />
<text  x="1132.76" y="273.5" ></text>
</g>
<g >
<title>firedrake.pointquery_utils.to_reference_coordinates (304,897 us, 0.02%)</title><rect x="1127.5" y="295" width="0.2" height="15.0" fill="rgb(136.703607128343,136.703607128343,153.878117508712)" rx="2" ry="2" />
<text  x="1130.49" y="305.5" ></text>
</g>
<g >
<title>ParLoopExecute (972,817 us, 0.07%)</title><rect x="950.7" y="247" width="0.8" height="15.0" fill="rgb(123.672540795938,123.672540795938,151.355975637924)" rx="2" ry="2" />
<text  x="953.68" y="257.5" ></text>
</g>
<g >
<title>MatMult (5,688,952 us, 0.41%)</title><rect x="996.2" y="247" width="4.9" height="15.0" fill="rgb(153.166205112422,120.940905861902,120.940905861902)" rx="2" ry="2" />
<text  x="999.24" y="257.5" ></text>
</g>
<g >
<title>ParLoopExecute (6,295,534 us, 0.46%)</title><rect x="989.7" y="295" width="5.4" height="15.0" fill="rgb(106.301476076833,144.596678982883,144.596678982883)" rx="2" ry="2" />
<text  x="992.68" y="305.5" ></text>
</g>
<g >
<title>ParLoopExecute (17,242,421 us, 1.26%)</title><rect x="315.1" y="151" width="14.8" height="15.0" fill="rgb(156.31881855852,145.110942281991,145.110942281991)" rx="2" ry="2" />
<text  x="318.08" y="161.5" ></text>
</g>
<g >
<title>pyop2.parloop.JITModule.compile (1,275,525 us, 0.09%)</title><rect x="133.8" y="135" width="1.1" height="15.0" fill="rgb(147.249052311213,159.750154274919,147.249052311213)" rx="2" ry="2" />
<text  x="136.81" y="145.5" ></text>
</g>
<g >
<title>MatMult (2,932,197 us, 0.21%)</title><rect x="949.0" y="183" width="2.5" height="15.0" fill="rgb(117.64811605268,147.538400458102,147.538400458102)" rx="2" ry="2" />
<text  x="952.00" y="193.5" ></text>
</g>
<g >
<title>pyop2.parloop.JITModule.compile (4,836,543 us, 0.35%)</title><rect x="1152.5" y="231" width="4.2" height="15.0" fill="rgb(127.432087747299,162.976171762068,127.432087747299)" rx="2" ry="2" />
<text  x="1155.54" y="241.5" ></text>
</g>
<g >
<title>firedrake.slate.slac.compiler.compile_expression (4,248,772 us, 0.31%)</title><rect x="826.8" y="199" width="3.6" height="15.0" fill="rgb(152.255415075689,152.255415075689,130.160857674491)" rx="2" ry="2" />
<text  x="829.77" y="209.5" ></text>
</g>
<g >
<title>firedrake.mg.interface.prolong (3,103,053 us, 0.23%)</title><rect x="998.5" y="279" width="2.6" height="15.0" fill="rgb(151.453690258339,151.453690258339,126.275575867336)" rx="2" ry="2" />
<text  x="1001.47" y="289.5" ></text>
</g>
<g >
<title>ParLoop_Cells_wrap_wrap_slate_loopy_knl_13 (132,580 us, 0.01%)</title><rect x="819.4" y="215" width="0.1" height="15.0" fill="rgb(150.316491884058,138.311010452899,150.316491884058)" rx="2" ry="2" />
<text  x="822.38" y="225.5" ></text>
</g>
<g >
<title>MatMult (3,759,528 us, 0.27%)</title><rect x="1001.7" y="231" width="3.2" height="15.0" fill="rgb(141.156211391263,160.742012099097,141.156211391263)" rx="2" ry="2" />
<text  x="1004.68" y="241.5" ></text>
</g>
<g >
<title>pyop2.parloop.JITModule.compile (10,350,354 us, 0.75%)</title><rect x="891.3" y="231" width="8.9" height="15.0" fill="rgb(139.577194069047,160.99906143062,139.577194069047)" rx="2" ry="2" />
<text  x="894.32" y="241.5" ></text>
</g>
<g >
<title>firedrake.variational_solver.NonlinearVariationalSolver.solve (136,185,377 us, 9.92%)</title><rect x="256.5" y="71" width="117.0" height="15.0" fill="rgb(154.935403739984,134.504762006547,134.504762006547)" rx="2" ry="2" />
<text  x="259.51" y="81.5" >firedrake.var..</text>
</g>
<g >
<title>firedrake.assemble.assemble (20,506,640 us, 1.49%)</title><rect x="1139.4" y="183" width="17.6" height="15.0" fill="rgb(132.383242531213,162.1701698205,132.383242531213)" rx="2" ry="2" />
<text  x="1142.40" y="193.5" ></text>
</g>
<g >
<title>ParLoopExecute (21,206,976 us, 1.54%)</title><rect x="1088.1" y="311" width="18.3" height="15.0" fill="rgb(109.423911490726,109.423911490726,148.59817641756)" rx="2" ry="2" />
<text  x="1091.14" y="321.5" ></text>
</g>
<g >
<title>KSPSolve (673,497,466 us, 49.04%)</title><rect x="578.4" y="119" width="578.6" height="15.0" fill="rgb(114.993887304955,114.993887304955,149.676236252572)" rx="2" ry="2" />
<text  x="581.40" y="129.5" >KSPSolve</text>
</g>
<g >
<title>firedrake.assemble.assemble (1,951,234 us, 0.14%)</title><rect x="949.8" y="215" width="1.7" height="15.0" fill="rgb(123.88185500283,149.154555000734,149.154555000734)" rx="2" ry="2" />
<text  x="952.84" y="225.5" ></text>
</g>
<g >
<title>SNESSolve (791,340,533 us, 57.62%)</title><rect x="510.1" y="103" width="679.9" height="15.0" fill="rgb(105.263355982427,144.327536736185,144.327536736185)" rx="2" ry="2" />
<text  x="513.11" y="113.5" >SNESSolve</text>
</g>
<g >
<title>pyop2.parloop.JITModule.compile (784,900 us, 0.06%)</title><rect x="1130.4" y="279" width="0.7" height="15.0" fill="rgb(155.802395940871,141.151702213348,141.151702213348)" rx="2" ry="2" />
<text  x="1133.44" y="289.5" ></text>
</g>
<g >
<title>pyop2.parloop.JITModule.compile (5,587,448 us, 0.41%)</title><rect x="1184.3" y="183" width="4.8" height="15.0" fill="rgb(131.132112395336,131.132112395336,152.79976368942)" rx="2" ry="2" />
<text  x="1187.31" y="193.5" ></text>
</g>
<g >
<title>ParLoop_Cells_wrap_wrap_slate_loopy_knl_0 (143,271 us, 0.01%)</title><rect x="891.2" y="231" width="0.1" height="15.0" fill="rgb(135.933842232703,161.592165217932,135.933842232703)" rx="2" ry="2" />
<text  x="894.19" y="241.5" ></text>
</g>
<g >
<title>firedrake.assemble.assemble_form (1,877,274 us, 0.14%)</title><rect x="1003.3" y="279" width="1.6" height="15.0" fill="rgb(151.55901595693,151.55901595693,126.78600040666)" rx="2" ry="2" />
<text  x="1006.30" y="289.5" ></text>
</g>
<g >
<title>SCForwardElim (86,059,172 us, 6.27%)</title><rect x="830.4" y="151" width="74.0" height="15.0" fill="rgb(146.556327397021,128.675588954865,146.556327397021)" rx="2" ry="2" />
<text  x="833.42" y="161.5" >SCForwa..</text>
</g>
<g >
<title>pyop2.parloop.JITModule.compile (9,520,699 us, 0.69%)</title><rect x="364.8" y="167" width="8.2" height="15.0" fill="rgb(156.390451571612,145.660128715689,145.660128715689)" rx="2" ry="2" />
<text  x="367.84" y="177.5" ></text>
</g>
<g >
<title>firedrake.tsfc_interface.compile_form (579,401 us, 0.04%)</title><rect x="373.0" y="151" width="0.5" height="15.0" fill="rgb(156.56901518067,147.029116385138,147.029116385138)" rx="2" ry="2" />
<text  x="376.02" y="161.5" ></text>
</g>
<g >
<title>firedrake.assemble_expressions.assemble_expression (5,175,242 us, 0.38%)</title><rect x="130.5" y="87" width="4.4" height="15.0" fill="rgb(146.897965970325,159.807307865296,146.897965970325)" rx="2" ry="2" />
<text  x="133.48" y="97.5" ></text>
</g>
<g >
<title>firedrake.assemble.assemble_form (29,749,916 us, 2.17%)</title><rect x="348.0" y="135" width="25.5" height="15.0" fill="rgb(145.373716286995,145.373716286995,155.556203152322)" rx="2" ry="2" />
<text  x="350.96" y="145.5" >f..</text>
</g>
<g >
<title>SNESJacobianEval (49,983,097 us, 3.64%)</title><rect x="330.6" y="103" width="42.9" height="15.0" fill="rgb(146.665162044416,155.061338307811,155.061338307811)" rx="2" ry="2" />
<text  x="333.57" y="113.5" >SNE..</text>
</g>
<g >
<title>firedrake.assemble.assemble_form (39,453,220 us, 2.87%)</title><rect x="870.5" y="199" width="33.9" height="15.0" fill="rgb(126.942612374914,149.948084689792,149.948084689792)" rx="2" ry="2" />
<text  x="873.47" y="209.5" >fi..</text>
</g>
<g >
<title>PCApply (39,963,671 us, 2.91%)</title><rect x="970.6" y="199" width="34.3" height="15.0" fill="rgb(108.149872327523,145.075892825654,145.075892825654)" rx="2" ry="2" />
<text  x="973.58" y="209.5" >PC..</text>
</g>
<g >
<title>MatResidual (4,387,491 us, 0.32%)</title><rect x="1001.1" y="215" width="3.8" height="15.0" fill="rgb(149.60787419725,159.366160014401,149.60787419725)" rx="2" ry="2" />
<text  x="1004.14" y="225.5" ></text>
</g>
<g >
<title>ParLoop_Cells_wrap_form1_cell_integral_otherwise (124,093 us, 0.01%)</title><rect x="1184.2" y="183" width="0.1" height="15.0" fill="rgb(150.044724127982,150.044724127982,119.447509235605)" rx="2" ry="2" />
<text  x="1187.21" y="193.5" ></text>
</g>
<g >
<title>pyop2.parloop.JITModule.compile (6,323,025 us, 0.46%)</title><rect x="250.0" y="151" width="5.4" height="15.0" fill="rgb(135.680431791197,135.680431791197,153.68008357249)" rx="2" ry="2" />
<text  x="252.99" y="161.5" ></text>
</g>
<g >
<title>PCApply (209,412,895 us, 15.25%)</title><rect x="951.5" y="183" width="179.9" height="15.0" fill="rgb(155.236381326721,136.812256838198,136.812256838198)" rx="2" ry="2" />
<text  x="954.52" y="193.5" >PCApply</text>
</g>
<g >
<title>pyop2.parloop.JITModule.compile (1,137,410 us, 0.08%)</title><rect x="846.1" y="215" width="0.9" height="15.0" fill="rgb(154.569591253762,131.700199612178,131.700199612178)" rx="2" ry="2" />
<text  x="849.06" y="225.5" ></text>
</g>
<g >
<title>ParLoopExecute (11,662,283 us, 0.85%)</title><rect x="1179.1" y="167" width="10.0" height="15.0" fill="rgb(137.733794967889,161.29914965639,137.733794967889)" rx="2" ry="2" />
<text  x="1182.10" y="177.5" ></text>
</g>
<g >
<title>firedrake.norms.norm (35,706,861 us, 2.60%)</title><rect x="225.6" y="87" width="30.7" height="15.0" fill="rgb(122.60338751346,148.823100466453,148.823100466453)" rx="2" ry="2" />
<text  x="228.62" y="97.5" >f..</text>
</g>
<g >
<title>firedrake.tsfc_interface.compile_form (1,697,357 us, 0.12%)</title><rect x="902.9" y="231" width="1.5" height="15.0" fill="rgb(152.666673849616,117.111166180388,117.111166180388)" rx="2" ry="2" />
<text  x="905.90" y="241.5" ></text>
</g>
<g >
<title>ParLoopExecute (19,054,273 us, 1.39%)</title><rect x="356.6" y="151" width="16.4" height="15.0" fill="rgb(131.084480225711,162.381596242326,131.084480225711)" rx="2" ry="2" />
<text  x="359.65" y="161.5" ></text>
</g>
<g >
<title>pyop2.parloop.JITModule.compile (8,470,830 us, 0.62%)</title><rect x="819.5" y="215" width="7.3" height="15.0" fill="rgb(149.026858751226,135.006325550016,149.026858751226)" rx="2" ry="2" />
<text  x="822.50" y="225.5" ></text>
</g>
<g >
<title>firedrake.slate.slac.compiler.compile_expression (451,802 us, 0.03%)</title><rect x="218.2" y="135" width="0.4" height="15.0" fill="rgb(152.207605646467,113.591643289584,113.591643289584)" rx="2" ry="2" />
<text  x="221.19" y="145.5" ></text>
</g>
<g >
<title>HybridProject (4,170,337 us, 0.30%)</title><rect x="725.0" y="167" width="3.6" height="15.0" fill="rgb(150.585272929826,159.207048592819,150.585272929826)" rx="2" ry="2" />
<text  x="728.04" y="177.5" ></text>
</g>
<g >
<title>ParLoop_Cells_wrap_form0_cell_integral_otherwise (118,885 us, 0.01%)</title><rect x="1184.1" y="183" width="0.1" height="15.0" fill="rgb(138.718849836648,153.001183290983,153.001183290983)" rx="2" ry="2" />
<text  x="1187.11" y="193.5" ></text>
</g>
<g >
<title>firedrake.assemble.assemble_form (48,576,673 us, 3.54%)</title><rect x="177.6" y="119" width="41.7" height="15.0" fill="rgb(150.196315686454,150.196315686454,120.182145249737)" rx="2" ry="2" />
<text  x="180.57" y="129.5" >fir..</text>
</g>
<g >
<title>firedrake.pointquery_utils.to_reference_coordinates (327,792 us, 0.02%)</title><rect x="1131.2" y="263" width="0.2" height="15.0" fill="rgb(138.038818073017,106.849471312105,138.038818073017)" rx="2" ry="2" />
<text  x="1134.16" y="273.5" ></text>
</g>
<g >
<title>firedrake.variational_solver.NonlinearVariationalSolver.__init__ (191,105 us, 0.01%)</title><rect x="256.3" y="71" width="0.2" height="15.0" fill="rgb(147.833522207497,159.655008012733,147.833522207497)" rx="2" ry="2" />
<text  x="259.35" y="81.5" ></text>
</g>
<g >
<title>firedrake.assemble.assemble_form (27,444,505 us, 2.00%)</title><rect x="307.0" y="135" width="23.6" height="15.0" fill="rgb(154.361055525695,154.361055525695,140.365115239909)" rx="2" ry="2" />
<text  x="309.99" y="145.5" >f..</text>
</g>
<g >
<title>PCSetUp (24,901,803 us, 1.81%)</title><rect x="1110.0" y="215" width="21.4" height="15.0" fill="rgb(147.785405126451,131.82510063653,147.785405126451)" rx="2" ry="2" />
<text  x="1113.05" y="225.5" ></text>
</g>
<g >
<title>firedrake.assemble.assemble (36,859,370 us, 2.68%)</title><rect x="298.9" y="119" width="31.7" height="15.0" fill="rgb(154.525642917306,131.363262366014,131.363262366014)" rx="2" ry="2" />
<text  x="301.91" y="129.5" >fi..</text>
</g>
<g >
<title>ParLoopExecute (3,486,933 us, 0.25%)</title><rect x="124.2" y="103" width="3.0" height="15.0" fill="rgb(145.631779683402,126.306435438718,145.631779683402)" rx="2" ry="2" />
<text  x="127.24" y="113.5" ></text>
</g>
<g >
<title>ParLoop_Cells_wrap_wrap_slate_loopy_knl_6 (206,048 us, 0.02%)</title><rect x="777.2" y="231" width="0.2" height="15.0" fill="rgb(107.917169739975,145.015562525179,145.015562525179)" rx="2" ry="2" />
<text  x="780.19" y="241.5" ></text>
</g>
<g >
<title>PCSetUp (5,073,329 us, 0.37%)</title><rect x="1157.0" y="119" width="4.4" height="15.0" fill="rgb(131.560421477623,131.560421477623,152.882662221476)" rx="2" ry="2" />
<text  x="1160.05" y="129.5" ></text>
</g>
<g >
<title>firedrake.tsfc_interface.compile_form (2,801,312 us, 0.20%)</title><rect x="790.3" y="231" width="2.4" height="15.0" fill="rgb(149.349537232215,149.349537232215,116.078526586888)" rx="2" ry="2" />
<text  x="793.28" y="241.5" ></text>
</g>
<g >
<title>firedrake (1,373,424,848 us, 100.00%)</title><rect x="10.0" y="55" width="1180.0" height="15.0" fill="rgb(155.842786807767,141.461365526213,141.461365526213)" rx="2" ry="2" />
<text  x="13.00" y="65.5" >firedrake</text>
</g>
<g >
<title>firedrake.norms.errornorm (43,056,874 us, 3.14%)</title><rect x="219.3" y="71" width="37.0" height="15.0" fill="rgb(110.011446207099,110.011446207099,148.711892814277)" rx="2" ry="2" />
<text  x="222.30" y="81.5" >fi..</text>
</g>
<g >
<title>firedrake.assemble.assemble_form (38,796,381 us, 2.82%)</title><rect x="1076.7" y="295" width="33.3" height="15.0" fill="rgb(148.762872115302,148.762872115302,113.235457174155)" rx="2" ry="2" />
<text  x="1079.71" y="305.5" >fi..</text>
</g>
<g >
<title>firedrake.matrix_free.operators.ImplicitMatrixContext.mult (2,441,685 us, 0.18%)</title><rect x="949.4" y="199" width="2.1" height="15.0" fill="rgb(153.993726078446,153.993726078446,138.584980226316)" rx="2" ry="2" />
<text  x="952.42" y="209.5" ></text>
</g>
<g >
<title>SNESFunctionEval (46,274,388 us, 3.37%)</title><rect x="290.8" y="103" width="39.8" height="15.0" fill="rgb(112.782063030684,146.276831156103,146.276831156103)" rx="2" ry="2" />
<text  x="293.82" y="113.5" >SNE..</text>
</g>
<g >
<title>firedrake.assemble.assemble_form (21,011,351 us, 1.53%)</title><rect x="238.2" y="119" width="18.1" height="15.0" fill="rgb(139.233915818422,139.233915818422,154.367854674533)" rx="2" ry="2" />
<text  x="241.24" y="129.5" ></text>
</g>
<g >
<title>firedrake.tsfc_interface.compile_form (1,623,492 us, 0.12%)</title><rect x="829.0" y="215" width="1.4" height="15.0" fill="rgb(132.179156581781,162.203393114594,132.179156581781)" rx="2" ry="2" />
<text  x="832.03" y="225.5" ></text>
</g>
<g >
<title>firedrake.tsfc_interface.compile_form (787,336 us, 0.06%)</title><rect x="329.9" y="151" width="0.7" height="15.0" fill="rgb(152.945378210901,119.247899616904,119.247899616904)" rx="2" ry="2" />
<text  x="332.90" y="161.5" ></text>
</g>
<g >
<title>pyop2.parloop.JITModule.compile (9,348,515 us, 0.68%)</title><rect x="1098.3" y="327" width="8.1" height="15.0" fill="rgb(134.385970206057,151.877844127496,151.877844127496)" rx="2" ry="2" />
<text  x="1101.33" y="337.5" ></text>
</g>
<g >
<title>firedrake.parloops.par_loop (3,122,892 us, 0.23%)</title><rect x="725.9" y="183" width="2.7" height="15.0" fill="rgb(123.041460742004,148.936675007186,148.936675007186)" rx="2" ry="2" />
<text  x="728.94" y="193.5" ></text>
</g>
<g >
<title>MatMult (78,696,307 us, 5.73%)</title><rect x="1042.4" y="247" width="67.6" height="15.0" fill="rgb(125.789623105347,125.789623105347,151.765733504261)" rx="2" ry="2" />
<text  x="1045.43" y="257.5" >MatMult</text>
</g>
<g >
<title>firedrake.matrix_free.operators.ImplicitMatrixContext.mult (65,395,121 us, 4.76%)</title><rect x="1053.9" y="263" width="56.1" height="15.0" fill="rgb(144.048248344563,122.248636382943,144.048248344563)" rx="2" ry="2" />
<text  x="1056.86" y="273.5" >fired..</text>
</g>
<g >
<title>firedrake.assemble.assemble (12,602,519 us, 0.92%)</title><rect x="984.3" y="263" width="10.8" height="15.0" fill="rgb(106.587714034387,144.67088882373,144.67088882373)" rx="2" ry="2" />
<text  x="987.26" y="273.5" ></text>
</g>
<g >
<title>pyop2.parloop.JITModule.compile (740,473 us, 0.05%)</title><rect x="1000.2" y="311" width="0.7" height="15.0" fill="rgb(125.523769447377,149.580236523394,149.580236523394)" rx="2" ry="2" />
<text  x="1003.21" y="321.5" ></text>
</g>
<g >
<title>pyop2.parloop.JITModule.compile (984,092 us, 0.07%)</title><rect x="1160.6" y="183" width="0.8" height="15.0" fill="rgb(108.266921536136,145.106238916776,145.106238916776)" rx="2" ry="2" />
<text  x="1163.56" y="193.5" ></text>
</g>
<g >
<title>all (1,373,424,848 us, 100%)</title><rect x="10.0" y="39" width="1180.0" height="15.0" fill="rgb(108.157349488547,145.077831348883,145.077831348883)" rx="2" ry="2" />
<text  x="13.00" y="49.5" ></text>
</g>
<g >
<title>firedrake.matrix_free.operators.ImplicitMatrixContext.mult (3,131,658 us, 0.23%)</title><rect x="1002.2" y="247" width="2.7" height="15.0" fill="rgb(140.330358210887,160.876453314507,140.330358210887)" rx="2" ry="2" />
<text  x="1005.22" y="257.5" ></text>
</g>
<g >
<title>DMCoarsen (16,843,375 us, 1.23%)</title><rect x="1113.3" y="231" width="14.4" height="15.0" fill="rgb(152.289503785269,114.219529020398,114.219529020398)" rx="2" ry="2" />
<text  x="1116.28" y="241.5" ></text>
</g>
<g >
<title>PCApply (7,044,938 us, 0.51%)</title><rect x="995.1" y="231" width="6.0" height="15.0" fill="rgb(134.137189564735,161.884643559229,134.137189564735)" rx="2" ry="2" />
<text  x="998.09" y="241.5" ></text>
</g>
<g >
<title>ParLoopExecute (1,482,997 us, 0.11%)</title><rect x="999.6" y="295" width="1.3" height="15.0" fill="rgb(144.918971942504,124.479865602666,144.918971942504)" rx="2" ry="2" />
<text  x="1002.58" y="305.5" ></text>
</g>
<g >
<title>ParLoopExecute (30,748,674 us, 2.24%)</title><rect x="191.8" y="135" width="26.4" height="15.0" fill="rgb(136.812824985912,161.449075002293,136.812824985912)" rx="2" ry="2" />
<text  x="194.78" y="145.5" >P..</text>
</g>
<g >
<title>RecoverFirstElim (74,564,340 us, 5.43%)</title><rect x="728.6" y="167" width="64.1" height="15.0" fill="rgb(132.901265844144,93.6844937256203,132.901265844144)" rx="2" ry="2" />
<text  x="731.63" y="177.5" >Recove..</text>
</g>
<g >
<title>firedrake.assemble.assemble (2,503,855 us, 0.18%)</title><rect x="1002.8" y="263" width="2.1" height="15.0" fill="rgb(142.608471925755,118.559209309747,142.608471925755)" rx="2" ry="2" />
<text  x="1005.76" y="273.5" ></text>
</g>
<g >
<title>ParLoopExecute (17,207,726 us, 1.25%)</title><rect x="812.0" y="199" width="14.8" height="15.0" fill="rgb(120.531975189214,120.531975189214,150.748124230171)" rx="2" ry="2" />
<text  x="814.99" y="209.5" ></text>
</g>
<g >
<title>firedrake.assemble.assemble (26,417,909 us, 1.92%)</title><rect x="1167.3" y="135" width="22.7" height="15.0" fill="rgb(150.773566498107,159.176396151471,150.773566498107)" rx="2" ry="2" />
<text  x="1170.30" y="145.5" ></text>
</g>
<g >
<title>SCSolve (294,104,071 us, 21.41%)</title><rect x="904.4" y="151" width="252.6" height="15.0" fill="rgb(142.186538992485,160.574284350061,142.186538992485)" rx="2" ry="2" />
<text  x="907.36" y="161.5" >SCSolve</text>
</g>
<g >
<title>firedrake.function.Function.project (98,207,222 us, 7.15%)</title><rect x="134.9" y="71" width="84.4" height="15.0" fill="rgb(152.174341742566,113.336620026337,113.336620026337)" rx="2" ry="2" />
<text  x="137.93" y="81.5" >firedrake..</text>
</g>
<g >
<title>firedrake.slate.slac.compiler.compile_expression (4,833,358 us, 0.35%)</title><rect x="900.2" y="215" width="4.2" height="15.0" fill="rgb(154.849985855622,154.849985855622,142.734546838782)" rx="2" ry="2" />
<text  x="903.21" y="225.5" ></text>
</g>
<g >
<title>firedrake.tsfc_interface.compile_form (157,223 us, 0.01%)</title><rect x="218.4" y="151" width="0.2" height="15.0" fill="rgb(155.891075040052,141.831575307065,141.831575307065)" rx="2" ry="2" />
<text  x="221.45" y="161.5" ></text>
</g>
<g >
<title>ParLoopExecute (2,275,592 us, 0.17%)</title><rect x="845.1" y="199" width="1.9" height="15.0" fill="rgb(122.437735085225,122.437735085225,151.116980984237)" rx="2" ry="2" />
<text  x="848.09" y="209.5" ></text>
</g>
<g >
<title>PCApply (601,918,287 us, 43.83%)</title><rect x="639.9" y="135" width="517.1" height="15.0" fill="rgb(122.964764934589,122.964764934589,151.218986761533)" rx="2" ry="2" />
<text  x="642.90" y="145.5" >PCApply</text>
</g>
<g >
<title>firedrake.assemble.assemble (59,322,754 us, 4.32%)</title><rect x="741.7" y="183" width="51.0" height="15.0" fill="rgb(124.309568819279,124.309568819279,151.479271384377)" rx="2" ry="2" />
<text  x="744.72" y="193.5" >fire..</text>
</g>
<g >
<title>SNESSolve (116,432,102 us, 8.48%)</title><rect x="273.5" y="87" width="100.0" height="15.0" fill="rgb(128.282585907431,150.29548523526,150.29548523526)" rx="2" ry="2" />
<text  x="276.48" y="97.5" >SNESSolve</text>
</g>
<g >
<title>firedrake.parloops.par_loop (2,960,052 us, 0.22%)</title><rect x="1158.9" y="151" width="2.5" height="15.0" fill="rgb(149.803610650101,149.803610650101,118.279036227414)" rx="2" ry="2" />
<text  x="1161.86" y="161.5" ></text>
</g>
<g >
<title>firedrake.assemble.assemble (65,113,115 us, 4.74%)</title><rect x="163.4" y="103" width="55.9" height="15.0" fill="rgb(148.442465119598,133.50881686897,148.442465119598)" rx="2" ry="2" />
<text  x="166.36" y="113.5" >fired..</text>
</g>
<g >
<title>ParLoop_Cells_wrap_wrap_slate_loopy_knl_3 (1,254,154 us, 0.09%)</title><rect x="1097.2" y="327" width="1.1" height="15.0" fill="rgb(117.92384697953,147.609886253952,147.609886253952)" rx="2" ry="2" />
<text  x="1100.25" y="337.5" ></text>
</g>
<g >
<title>PCSetUp (421,846 us, 0.03%)</title><rect x="290.5" y="103" width="0.3" height="15.0" fill="rgb(154.380615130928,130.251382670448,130.251382670448)" rx="2" ry="2" />
<text  x="293.45" y="113.5" ></text>
</g>
<g >
<title>KSPSolve (235,018,879 us, 17.11%)</title><rect x="929.5" y="167" width="201.9" height="15.0" fill="rgb(145.878096495501,145.878096495501,155.653825128161)" rx="2" ry="2" />
<text  x="932.52" y="177.5" >KSPSolve</text>
</g>
<g >
<title>firedrake.projection.project (81,660,067 us, 5.95%)</title><rect x="149.1" y="87" width="70.2" height="15.0" fill="rgb(155.608302984215,155.608302984215,146.40946830812)" rx="2" ry="2" />
<text  x="152.14" y="97.5" >firedra..</text>
</g>
<g >
<title>firedrake.assemble.assemble (6,477,012 us, 0.47%)</title><rect x="129.4" y="71" width="5.5" height="15.0" fill="rgb(149.571920405322,149.571920405322,117.156229656558)" rx="2" ry="2" />
<text  x="132.36" y="81.5" ></text>
</g>
<g >
<title>firedrake.parloops.par_loop (3,419,874 us, 0.25%)</title><rect x="844.1" y="183" width="2.9" height="15.0" fill="rgb(149.574260747428,149.574260747428,117.167571314461)" rx="2" ry="2" />
<text  x="847.10" y="193.5" ></text>
</g>
</g>
</svg>
